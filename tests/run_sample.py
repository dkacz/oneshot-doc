#!/usr/bin/env python3
"""Run the bundled synthetic oneshot-doc sample across selected themes."""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS_DIR = ROOT / "assets"
SAMPLE_DIR = ROOT / "tests" / "sample"

sys.path.insert(0, str(ASSETS_DIR))
from palette import font_template_values, theme_names


def parse_theme_list(raw: str) -> list[str]:
    if raw.strip().casefold() == "all":
        return theme_names()
    themes = [item.strip() for item in raw.split(",") if item.strip()]
    if not themes:
        raise ValueError("--themes must name at least one theme")
    known = set(theme_names())
    unknown = [theme for theme in themes if theme not in known]
    if unknown:
        raise ValueError(f"unknown theme(s): {', '.join(unknown)}")
    return themes


def render_header(theme: str, out_path: Path) -> None:
    values = font_template_values(theme)
    values.update(
        {
            "GEOMETRY_OPTIONS": "top=20mm,bottom=20mm,left=24mm,right=24mm",
            "LINESPREAD": "1.0",
            "PARSKIP": "0.34em",
            "SECNUMDEPTH": "0",
            "KIND_LABEL": "SAMPLE",
            "DATE_LABEL": "",
            "TITLE_SIZE": "Huge",
            "HEADER_LEFT": "Theme sample",
        }
    )
    text = (ASSETS_DIR / "themes" / theme / "header.tex").read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")


def run_command(label: str, cmd: list[str], cwd: Path) -> int:
    print(f"\n[{label}]")
    print("  $ " + " ".join(cmd))
    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(result.stderr.rstrip(), file=sys.stderr)
    if result.returncode == 0:
        print(f"  OK: {label}")
    else:
        print(f"  FAIL: {label} exited {result.returncode}")
    return result.returncode


def run_theme(theme: str, run_root: Path) -> int:
    work_dir = run_root / theme
    shutil.copytree(
        SAMPLE_DIR,
        work_dir,
        ignore=shutil.ignore_patterns("__pycache__", "*.png", "*.pdf", "*.docx", "qa", "formatting"),
    )
    render_header(theme, work_dir / "formatting" / "header.tex")

    figure_rc = run_command(
        f"figure {theme}",
        [sys.executable, str(work_dir / "figures" / "make_figure.py"), "--theme", theme],
        work_dir,
    )
    if figure_rc != 0:
        return figure_rc

    return run_command(
        f"pipeline {theme}",
        [
            sys.executable,
            str(ROOT / "checks" / "run_pipeline.py"),
            "--qmd",
            "sample.qmd",
            "--budget",
            "2",
            "--formats",
            "pdf,docx",
            "--theme",
            theme,
            "--gates-args=--parity-warn-only",
        ],
        work_dir,
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run synthetic sample themes.")
    parser.add_argument("--themes", default=",".join(theme_names()))
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        themes = parse_theme_list(args.themes)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    failed: list[str] = []
    with tempfile.TemporaryDirectory(prefix=".oneshot-sample-", dir=ROOT) as temp_dir:
        run_root = Path(temp_dir)
        print(f"sample run root: {run_root}")
        for theme in themes:
            rc = run_theme(theme, run_root)
            if rc != 0:
                failed.append(theme)

    if failed:
        print("\nSample result: FAIL")
        print("Failed themes: " + ", ".join(failed))
        return 1

    print("\nSample result: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
