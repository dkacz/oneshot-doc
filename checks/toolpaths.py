"""Shared executable resolution for oneshot-doc checks.

The resolver returns argv prefixes rather than strings so callers can pass the
result directly to subprocess without shell=True on every platform.
"""
from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
from typing import Any, Iterator, Sequence


def _cmd_wrapper(path: str) -> list[str]:
    if Path(path).suffix.casefold() in {".cmd", ".bat"}:
        return ["cmd", "/c", path]
    return [path]


def _soffice_fallbacks() -> list[Path]:
    paths = [
        Path(r"C:\Program Files\LibreOffice\program\soffice.exe"),
        Path(r"C:\Program Files (x86)\LibreOffice\program\soffice.exe"),
        Path("/Applications/LibreOffice.app/Contents/MacOS/soffice"),
    ]
    local_appdata = os.environ.get("LOCALAPPDATA")
    if local_appdata:
        paths.insert(2, Path(local_appdata) / "Programs" / "LibreOffice" / "program" / "soffice.exe")
    return paths


def _extra_tool_dirs() -> Iterator[Path]:
    home = Path.home()
    tex_roots = [
        home / "Library" / "TinyTeX" / "bin",
        home / ".TinyTeX" / "bin",
        home / "TinyTeX" / "bin",
    ]
    for env_name in ("APPDATA", "LOCALAPPDATA"):
        value = os.environ.get(env_name)
        if value:
            tex_roots.append(Path(value) / "TinyTeX" / "bin")

    for tex_root in tex_roots:
        if tex_root.is_dir():
            yield tex_root
            for child in tex_root.iterdir():
                if child.is_dir():
                    yield child

    for path in (
        Path("/Library/TeX/texbin"),
        Path("/Applications/LibreOffice.app/Contents/MacOS"),
        Path("/Applications/quarto/bin"),
    ):
        if path.is_dir():
            yield path


def _candidate_names(name: str) -> list[str]:
    if Path(name).suffix:
        return [name]
    names = [name]
    if os.name == "nt":
        for ext in os.environ.get("PATHEXT", ".COM;.EXE;.BAT;.CMD").split(os.pathsep):
            ext = ext.strip()
            if ext:
                names.append(name + ext.lower())
                names.append(name + ext.upper())
    return list(dict.fromkeys(names))


def resolved_tool_path(name: str) -> str | None:
    """Return the executable path found for *name*, or None if it is unresolved."""
    found = shutil.which(name)
    if found:
        return found

    for directory in _extra_tool_dirs():
        for candidate_name in _candidate_names(name):
            candidate = directory / candidate_name
            if candidate.is_file() and os.access(candidate, os.X_OK):
                return str(candidate)

    if name == "soffice":
        for path in _soffice_fallbacks():
            if path.is_file():
                return str(path)
    return None


def resolve_tool(name: str) -> list[str]:
    """Return an argv prefix for *name* with Windows batch wrappers handled."""
    found = resolved_tool_path(name)
    if found:
        return _cmd_wrapper(found)
    return [name]


def run_tool(name: str, args: Sequence[str | os.PathLike[str]], **kw: Any) -> subprocess.CompletedProcess[Any]:
    """Run *name* with *args* using the shared resolver."""
    if kw.get("text") or kw.get("universal_newlines"):
        kw.setdefault("encoding", "utf-8")
        kw.setdefault("errors", "replace")
    return subprocess.run(resolve_tool(name) + [str(arg) for arg in args], **kw)
