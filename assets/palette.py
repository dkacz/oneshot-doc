"""oneshot-doc: house palette and Matplotlib setup for document figures.

Import from figure scripts:

    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path("path/to/oneshot-doc/assets").resolve()))
    from palette import WPBLUE, WPRULE, WPGRAY, WPLIGHT, BRICK, setup_fonts, save

Every figure script should call setup_fonts() once, draw with the palette
colours only, and finish with save(fig, path). Keep one intention per figure.
"""
from pathlib import Path
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

THEMES = {
    "think-tank": {
        "primary": "#253B59",
        "rule": "#7D93AD",
        "gray": "#4B5563",
        "light": "#EEF3F8",
        "accent": "#A6442C",
        "body_family": "serif",
        "heading_family": "sans",
    },
    "academic": {
        "primary": "#2B2B2B",
        "rule": "#9A9A9A",
        "gray": "#444444",
        "light": "#F4F2EC",
        "accent": "#7A2E2E",
        "body_family": "serif",
        "heading_family": "serif",
    },
    "minimal": {
        "primary": "#111827",
        "rule": "#D1D5DB",
        "gray": "#6B7280",
        "light": "#F9FAFB",
        "accent": "#0F766E",
        "body_family": "sans",
        "heading_family": "sans",
    },
}

WPBLUE = THEMES["think-tank"]["primary"]   # primary: titles, main series, emphasis
WPRULE = THEMES["think-tank"]["rule"]      # secondary: rules, comparison series, frames
WPGRAY = THEMES["think-tank"]["gray"]      # text grey: labels, annotations
WPLIGHT = THEMES["think-tank"]["light"]    # light background fill
BRICK = THEMES["think-tank"]["accent"]     # warning/contrast accent, use sparingly

SANS_FAMILY = "Source Sans 3"
SERIF_FAMILY = "Source Serif 4"

SANS_DIR = Path.home() / ".fonts" / "source-sans"
SERIF_DIR = Path.home() / ".fonts" / "source-serif"


class FontResolutionError(RuntimeError):
    """Raised when the Source font directories cannot be located."""


def theme_names() -> list[str]:
    """Return available visual theme names in declaration order."""
    return list(THEMES)


def _normalize_hex(value: str) -> str:
    raw = value.strip()
    if raw.startswith("#"):
        raw = raw[1:]
    if len(raw) != 6 or any(ch not in "0123456789abcdefABCDEF" for ch in raw):
        raise ValueError(f"Expected a 6 digit hex colour, got: {value!r}")
    return "#" + raw.upper()


def get_theme(name: str = "think-tank", accent: str | None = None) -> dict[str, str]:
    """Return a copy of a named visual theme, optionally overriding the accent."""
    if name not in THEMES:
        raise ValueError(f"Unknown theme {name!r}. Available themes: {', '.join(theme_names())}")
    theme = dict(THEMES[name])
    if accent is not None:
        theme["accent"] = _normalize_hex(accent)
    return theme


def theme_colors(name: str = "think-tank", accent: str | None = None) -> dict[str, str]:
    """Return only the colour keys for a named theme."""
    theme = get_theme(name, accent)
    return {key: theme[key] for key in ("primary", "rule", "gray", "light", "accent")}


def _font_files(directory: Path) -> list[Path]:
    if not directory.is_dir():
        return []
    return sorted([*directory.glob("*.otf"), *directory.glob("*.ttf")])


def _compact(value: str) -> str:
    return "".join(ch for ch in value.casefold() if ch.isalnum())


def _font_name(path: Path) -> str:
    try:
        return font_manager.FontProperties(fname=str(path)).get_name()
    except Exception:
        return ""


def _has_family(directory: Path, family: str) -> bool:
    target = _compact(family)
    for font_path in _font_files(directory):
        candidates = {item for item in (_compact(font_path.stem), _compact(_font_name(font_path))) if item}
        if any(target in candidate or candidate in target for candidate in candidates):
            return True
    return False


def _fontspec_dir(path: Path) -> str:
    value = path.expanduser().resolve().as_posix()
    return value if value.endswith("/") else value + "/"


def _font_error(reason: str | None = None) -> str:
    parts = []
    if reason:
        parts.append(reason)
    parts.append(
        "Source fonts not found. Install Source Sans 3 and Source Serif 4 "
        "(SIL Open Font License) from github.com/adobe-fonts/source-sans "
        "and github.com/adobe-fonts/source-serif."
    )
    parts.append(
        "Set ONESHOT_FONTS_DIR to a directory containing source-sans/ and "
        "source-serif/ subdirectories, or put both families' .otf/.ttf files "
        "directly in that directory."
    )
    return " ".join(parts)


def _env_font_dirs() -> tuple[Path, Path] | None:
    raw = os.environ.get("ONESHOT_FONTS_DIR")
    if not raw:
        return None
    root = Path(raw).expanduser()
    if not root.is_dir():
        raise FontResolutionError(_font_error(f"ONESHOT_FONTS_DIR is not a directory: {root}"))

    subdirs = (root / "source-sans", root / "source-serif")
    if all(_font_files(directory) for directory in subdirs):
        return subdirs
    if _has_family(root, SANS_FAMILY) and _has_family(root, SERIF_FAMILY):
        return root, root
    raise FontResolutionError(
        _font_error(
            f"ONESHOT_FONTS_DIR does not contain source-sans/ and source-serif/ "
            f"with font files, or direct files for both {SANS_FAMILY} and {SERIF_FAMILY}: {root}"
        )
    )


def _home_font_dirs() -> tuple[Path, Path] | None:
    dirs = (Path.home() / ".fonts" / "source-sans", Path.home() / ".fonts" / "source-serif")
    return dirs if all(_font_files(directory) for directory in dirs) else None


def _system_font_dirs() -> tuple[Path, Path] | None:
    dirs = []
    for family in (SANS_FAMILY, SERIF_FAMILY):
        try:
            font_path = Path(
                font_manager.findfont(
                    font_manager.FontProperties(family=family),
                    fallback_to_default=False,
                )
            )
        except Exception:
            return None
        if not font_path.is_file():
            return None
        dirs.append(font_path.parent)
    return dirs[0], dirs[1]


def resolve_font_dirs() -> tuple[Path, Path]:
    """Return the Source Sans and Source Serif directories in priority order."""
    global SANS_DIR, SERIF_DIR

    dirs = _env_font_dirs() or _home_font_dirs() or _system_font_dirs()
    if dirs is None:
        raise FontResolutionError(_font_error())
    SANS_DIR, SERIF_DIR = dirs
    return dirs


def font_dir_strings() -> tuple[str, str]:
    """Return Source Sans and Source Serif directories for template replacement."""
    sans_dir, serif_dir = resolve_font_dirs()
    return _fontspec_dir(sans_dir), _fontspec_dir(serif_dir)


def font_template_values(theme: str = "think-tank", accent: str | None = None) -> dict[str, str]:
    """Return replacement values for theme header templates."""
    sans_dir, serif_dir = font_dir_strings()
    colours = theme_colors(theme, accent)
    values = {"SANS_FONT_DIR": sans_dir, "SERIF_FONT_DIR": serif_dir}
    values.update({key.upper(): value.lstrip("#") for key, value in colours.items()})
    return values


def setup_fonts(family: str | None = None, theme: str = "think-tank") -> None:
    """Register Source fonts and set matplotlib defaults for document figures."""
    theme_data = get_theme(theme)
    sans_dir, serif_dir = resolve_font_dirs()
    for d in dict.fromkeys((sans_dir, serif_dir)):
        for f in _font_files(d):
            try:
                font_manager.fontManager.addfont(str(f))
            except RuntimeError:
                # Some installed variable-font files are unreadable by Matplotlib.
                # Static Source font files in the same directory are enough.
                continue
    plt.rcParams["font.family"] = family or SANS_FAMILY
    plt.rcParams["axes.edgecolor"] = theme_data["gray"]
    plt.rcParams["axes.labelcolor"] = theme_data["gray"]
    plt.rcParams["xtick.color"] = theme_data["gray"]
    plt.rcParams["ytick.color"] = theme_data["gray"]
    plt.rcParams["text.color"] = theme_data["gray"]
    plt.rcParams["axes.spines.top"] = False
    plt.rcParams["axes.spines.right"] = False
    plt.rcParams["grid.color"] = theme_data["rule"]
    plt.rcParams["grid.alpha"] = 0.35
    plt.rcParams["grid.linewidth"] = 0.5


def save(fig, path, dpi: int = 300) -> None:
    """Save with house defaults; tight layout is the caller's job when needed."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor="white")
    plt.close(fig)
