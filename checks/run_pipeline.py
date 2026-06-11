"""Run one deterministic oneshot-doc production render cycle.

Usage:
    python3 checks/run_pipeline.py --qmd doc.qmd --budget 4 \
        --formats pdf,docx \
        --postprocess-args '--geometry "A4,top=20,bottom=20,left=24,right=24" --boxes-to-tables' \
        --gates-args '--parity-warn-only' \
        --outdir qa

The runner renders once, post-processes once, and runs gates once. It does not
repair the document and does not iterate; the producer owns every next cycle.
"""

from __future__ import annotations

import argparse
import re
import shlex
import subprocess
import sys
import time
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
ASSETS_DIR = SKILL_ROOT / "assets"
BUILD_REFERENCE = ASSETS_DIR / "build_reference_docx.py"
DOCX_POSTPROCESS = ASSETS_DIR / "docx_postprocess.py"
QA_GATES = SKILL_ROOT / "checks" / "qa_gates.py"
PYTHON = sys.executable or "python3"
sys.path.insert(0, str(ASSETS_DIR))
from palette import get_theme, theme_names


class PipelineError(Exception):
    """Controlled pipeline failure with a user-facing message."""


def shell_join(cmd: list[str]) -> str:
    return " ".join(shlex.quote(str(part)) for part in cmd)


def tail_lines(text: str, count: int = 30) -> str:
    lines = text.splitlines()
    return "\n".join(lines[-count:])


def rel_to(path: Path, base: Path) -> str:
    try:
        return str(path.relative_to(base))
    except ValueError:
        return str(path)


def parse_formats(raw: str) -> list[str]:
    formats = [item.strip().lower() for item in raw.split(",") if item.strip()]
    if not formats:
        raise PipelineError("--formats must contain pdf or pdf,docx")
    bad = [item for item in formats if item not in {"pdf", "docx"}]
    if bad:
        raise PipelineError(f"unsupported format(s): {', '.join(bad)}")
    ordered = []
    for item in formats:
        if item not in ordered:
            ordered.append(item)
    if "pdf" not in ordered:
        raise PipelineError("pdf is required because qa_gates.py always gates a PDF")
    return ordered


def split_extra_args(raw: str, flag_name: str) -> list[str]:
    if not raw:
        return []
    try:
        return shlex.split(raw)
    except ValueError as exc:
        raise PipelineError(f"could not parse {flag_name}: {exc}") from exc


def frontmatter(qmd: Path) -> str:
    lines = qmd.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return ""
    for idx, line in enumerate(lines[1:], 1):
        if line.strip() in {"---", "..."}:
            return "\n".join(lines[1:idx])
    return ""


def has_reference_doc(qmd: Path) -> bool:
    meta = frontmatter(qmd)
    for line in meta.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if re.match(r"reference-doc\s*:", stripped):
            return True
    return False


def resolve_outdir(raw: Path, docdir: Path) -> Path:
    return raw if raw.is_absolute() else docdir / raw


def run_step(
    label: str,
    cmd: list[str],
    cwd: Path,
    *,
    show_stdout: bool = False,
    allow_failure: bool = False,
) -> subprocess.CompletedProcess[str]:
    print(f"\n[{label}]")
    print(f"  $ {shell_join(cmd)}")
    try:
        result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    except FileNotFoundError as exc:
        raise PipelineError(f"command not found: {cmd[0]}") from exc

    if result.returncode == 0:
        print("  OK")
        if show_stdout and result.stdout.strip():
            print(result.stdout.rstrip())
        return result

    print(f"  FAIL (exit {result.returncode})")
    stderr = result.stderr.strip()
    stdout = result.stdout.strip()
    if stderr:
        print("  stderr tail:")
        print(tail_lines(stderr))
    elif stdout and not (allow_failure and show_stdout):
        print("  stdout tail:")
        print(tail_lines(stdout))
    if allow_failure:
        if show_stdout and stdout:
            print(stdout)
        return result
    raise PipelineError(f"{label} failed")


def locate_output(qmd: Path, suffix: str, started_at: float) -> Path:
    expected = qmd.with_suffix(suffix)
    threshold = started_at - 2.0
    if expected.exists() and expected.stat().st_mtime >= threshold:
        return expected

    candidates = [
        path
        for path in qmd.parent.glob(f"*{suffix}")
        if path.is_file() and path.stat().st_mtime >= threshold
    ]
    if len(candidates) == 1:
        return candidates[0]
    if expected.exists():
        return expected
    detail = ", ".join(path.name for path in candidates) or "none"
    raise PipelineError(f"could not locate rendered {suffix} output; recent candidates: {detail}")


def ensure_reference_doc(qmd: Path, theme: str, accent: str | None) -> Path:
    reference = qmd.parent / "formatting" / "reference.docx"
    marker = qmd.parent / "formatting" / "reference.theme.txt"
    marker_value = f"{theme}|{accent or ''}"
    should_build = not reference.exists()
    reason = "missing"
    if reference.exists() and reference.stat().st_mtime < BUILD_REFERENCE.stat().st_mtime:
        should_build = True
        reason = "older than build_reference_docx.py"
    if not marker.exists():
        should_build = True
        reason = "theme marker missing"
    elif marker.read_text(encoding="utf-8").strip() != marker_value:
        should_build = True
        reason = "theme marker changed"

    if should_build:
        cmd = [PYTHON, str(BUILD_REFERENCE), rel_to(reference, qmd.parent), "--theme", theme]
        if accent:
            cmd.extend(["--accent", accent])
        run_step(
            f"Build DOCX reference ({reason})",
            cmd,
            qmd.parent,
            show_stdout=True,
        )
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.write_text(marker_value + "\n", encoding="utf-8")
    else:
        print("\n[Build DOCX reference]")
        print(f"  OK ({rel_to(reference, qmd.parent)} is current)")
    return reference


def render_pdf(qmd: Path) -> Path:
    started = time.time()
    run_step("Render PDF", ["quarto", "render", qmd.name, "--to", "pdf"], qmd.parent)
    return locate_output(qmd, ".pdf", started)


def render_docx(qmd: Path, reference: Path) -> Path:
    cmd = ["quarto", "render", qmd.name, "--to", "docx"]
    if has_reference_doc(qmd):
        print("\n[DOCX reference binding]")
        print("  OK (qmd YAML already declares reference-doc; runner will not override it)")
    else:
        cmd.extend(["--reference-doc", rel_to(reference, qmd.parent)])

    started = time.time()
    run_step("Render DOCX", cmd, qmd.parent)
    return locate_output(qmd, ".docx", started)


def run_pipeline(args: argparse.Namespace) -> int:
    qmd = args.qmd.expanduser().resolve()
    if not qmd.exists():
        raise PipelineError(f"qmd not found: {qmd}")
    if args.budget < 1:
        raise PipelineError("--budget must be a positive integer")

    formats = parse_formats(args.formats)
    try:
        get_theme(args.theme, args.accent)
    except ValueError as exc:
        raise PipelineError(str(exc)) from exc
    postprocess_args = split_extra_args(args.postprocess_args, "--postprocess-args")
    postprocess_args.extend(["--theme", args.theme])
    if args.accent:
        postprocess_args.extend(["--accent", args.accent])
    gates_args = split_extra_args(args.gates_args, "--gates-args")
    outdir = resolve_outdir(args.outdir.expanduser(), qmd.parent)

    print("oneshot-doc production pipeline")
    print(f"  qmd: {qmd}")
    print(f"  budget: {args.budget}")
    print(f"  formats: {','.join(formats)}")
    print(f"  theme: {args.theme}|{args.accent or ''}")
    print(f"  outdir: {outdir}")

    pdf = render_pdf(qmd)
    docx = None
    if "docx" in formats:
        reference = ensure_reference_doc(qmd, args.theme, args.accent)
        docx = render_docx(qmd, reference)
        run_step(
            "DOCX postprocess",
            [PYTHON, str(DOCX_POSTPROCESS), rel_to(docx, qmd.parent), *postprocess_args],
            qmd.parent,
            show_stdout=True,
        )

    numbers = qmd.parent / "NUMBERS.md"
    gates_cmd = [
        PYTHON,
        str(QA_GATES),
        "--qmd",
        qmd.name,
        "--pdf",
        rel_to(pdf, qmd.parent),
        "--budget",
        str(args.budget),
        "--outdir",
        rel_to(outdir, qmd.parent),
    ]
    if docx is not None:
        gates_cmd.extend(["--docx", rel_to(docx, qmd.parent)])
    if numbers.exists():
        gates_cmd.extend(["--numbers", rel_to(numbers, qmd.parent)])
    gates_cmd.extend(gates_args)

    gates = run_step("QA gates", gates_cmd, qmd.parent, show_stdout=True, allow_failure=True)
    status = "PASS" if gates.returncode == 0 else "FAIL"
    print(f"\nPipeline result: {status}")
    return 0 if gates.returncode == 0 else 1


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run one oneshot-doc production render cycle.")
    parser.add_argument("--qmd", required=True, type=Path)
    parser.add_argument("--budget", required=True, type=int)
    parser.add_argument("--formats", default="pdf,docx", help="Comma-separated formats: pdf or pdf,docx.")
    parser.add_argument(
        "--postprocess-args",
        default="",
        help="Argument string passed through to assets/docx_postprocess.py after the DOCX path.",
    )
    parser.add_argument(
        "--gates-args",
        default="",
        help="Argument string passed through to checks/qa_gates.py after the canonical arguments.",
    )
    parser.add_argument("--outdir", type=Path, default=Path("qa"))
    parser.add_argument("--theme", default="think-tank", choices=theme_names())
    parser.add_argument("--accent", help="Override the theme accent with a 6 digit hex colour.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    try:
        return run_pipeline(parse_args(sys.argv[1:] if argv is None else argv))
    except PipelineError as exc:
        print(f"\nPipeline result: FAIL")
        print(f"Reason: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
