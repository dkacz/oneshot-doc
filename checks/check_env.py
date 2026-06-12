#!/usr/bin/env python3
"""Check the local runtime needed by oneshot-doc."""
from __future__ import annotations

import importlib
import importlib.util
from pathlib import Path
import sys

from toolpaths import resolved_tool_path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

ROOT = Path(__file__).resolve().parents[1]
ASSETS_DIR = ROOT / "assets"
PALETTE_PATH = ASSETS_DIR / "palette.py"


class CheckResult:
    def __init__(self, name: str, ok: bool, detail: str) -> None:
        self.name = name
        self.ok = ok
        self.detail = detail

    @property
    def status(self) -> str:
        return "OK" if self.ok else "MISSING"

def check_tool(name: str) -> CheckResult:
    found = resolved_tool_path(name)
    return CheckResult(name, found is not None, found or "not found")


def check_latex_engine() -> CheckResult:
    engines = []
    for name in ("xelatex", "lualatex"):
        found = resolved_tool_path(name)
        if found:
            engines.append(f"{name}: {found}")
    return CheckResult(
        "xelatex or lualatex",
        bool(engines),
        "; ".join(engines) if engines else "not found",
    )


def check_python_import(module_name: str) -> CheckResult:
    try:
        module = importlib.import_module(module_name)
    except Exception as exc:
        return CheckResult(f"python import: {module_name}", False, f"{type(exc).__name__}: {exc}")
    detail = getattr(module, "__file__", None) or "built-in"
    return CheckResult(f"python import: {module_name}", True, str(detail))


def load_palette_module():
    spec = importlib.util.spec_from_file_location("oneshot_doc_palette", PALETTE_PATH)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {PALETTE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_fonts() -> CheckResult:
    try:
        palette = load_palette_module()
        sans_dir, serif_dir = palette.resolve_font_dirs()
    except Exception as exc:
        return CheckResult("Source Sans 3 and Source Serif 4 fonts", False, f"{type(exc).__name__}: {exc}")
    return CheckResult(
        "Source Sans 3 and Source Serif 4 fonts",
        True,
        f"Source Sans: {sans_dir}; Source Serif: {serif_dir}",
    )


def print_table(results: list[CheckResult]) -> None:
    name_width = max(len("Check"), *(len(result.name) for result in results))
    status_width = len("MISSING")
    print(f"{'Check':<{name_width}}  {'Status':<{status_width}}  Detail")
    print(f"{'-' * name_width}  {'-' * status_width}  {'-' * 40}")
    for result in results:
        print(f"{result.name:<{name_width}}  {result.status:<{status_width}}  {result.detail}")


def print_install_hints(results: list[CheckResult]) -> None:
    missing = [result.name for result in results if not result.ok]
    if not missing:
        print()
        print("All checks passed.")
        return

    print()
    print("Missing checks: " + ", ".join(missing))
    print(
        "Install missing system tools on macOS: brew install quarto pandoc poppler; "
        "brew install --cask libreoffice; quarto install tinytex"
    )
    print(
        "Install missing system tools on Debian/Ubuntu: install Quarto from the .deb at "
        "https://quarto.org/docs/get-started/; sudo apt install pandoc poppler-utils "
        "libreoffice texlive-xetex texlive-luatex"
    )
    print(
        "Install missing system tools on Windows: winget install Quarto.Quarto "
        "JohnMacFarlane.Pandoc TheDocumentFoundation.LibreOffice; quarto install tinytex; "
        "Poppler from https://github.com/oschwartz10612/poppler-windows (add bin\\ to PATH); "
        "python -m pip install python-docx matplotlib pypdf; install fonts to "
        "%USERPROFILE%\\.fonts\\source-sans and %USERPROFILE%\\.fonts\\source-serif, "
        "or set ONESHOT_FONTS_DIR."
    )
    print("Install missing Python packages: python3 -m pip install python-docx matplotlib pypdf")
    print(
        "If pip refuses with 'externally-managed-environment' (PEP 668): on Debian/Ubuntu "
        "prefer sudo apt install python3-docx python3-matplotlib python3-pypdf; otherwise "
        "add --break-system-packages, or use a virtual environment and run the skill "
        "scripts with that environment's python3."
    )
    print(
        "Install missing fonts: download Source Sans 3 and Source Serif 4 from "
        "github.com/adobe-fonts into ~/.fonts/source-sans and ~/.fonts/source-serif, "
        "or set ONESHOT_FONTS_DIR."
    )


def main() -> int:
    results = [
        check_tool("quarto"),
        check_latex_engine(),
        check_tool("pandoc"),
        check_tool("soffice"),
        check_tool("pdftotext"),
        check_tool("pdftoppm"),
        check_tool("pdffonts"),
        check_python_import("docx"),
        check_python_import("matplotlib"),
        check_python_import("pypdf"),
        check_fonts(),
    ]
    print(f"oneshot-doc environment check: {ROOT}")
    print()
    print_table(results)
    print_install_hints(results)
    return 0 if all(result.ok for result in results) else 1


if __name__ == "__main__":
    sys.exit(main())
