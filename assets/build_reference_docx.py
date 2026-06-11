"""Build a house-styled reference.docx for Pandoc/Quarto DOCX rendering.

Usage:
    python3 build_reference_docx.py /path/to/reference.docx

Starts from pandoc's default reference document and restyles it with the
house palette (WPBlue headings in Source Sans 3, body in Source Serif 4).
The output is passed to quarto/pandoc via `reference-doc:` in the qmd YAML.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Pt, RGBColor

try:
    from palette import WPBLUE, WPGRAY, WPLIGHT, WPRULE
except ImportError:  # pragma: no cover - only used when copied away from assets/
    WPBLUE = "#253B59"
    WPGRAY = "#4B5563"
    WPLIGHT = "#EEF3F8"
    WPRULE = "#7D93AD"

SANS = "Source Sans 3"
SERIF = "Source Serif 4"
MONO = "Consolas"


def rgb(hex_color: str) -> RGBColor:
    value = hex_color.lstrip("#")
    return RGBColor(int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16))


def set_font(style, name, size=None, color=None, bold=None, italic=None):
    f = style.font
    f.name = name
    # Cover hAnsi/cs so Word uses the family for all script ranges.
    rpr = style.element.get_or_add_rPr()
    rfonts = rpr.get_or_add_rFonts()
    for attr in ("ascii", "hAnsi", "cs"):
        rfonts.set(
            "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}" + attr,
            name,
        )
    if size is not None:
        f.size = Pt(size)
    if color is not None:
        f.color.rgb = color
    if bold is not None:
        f.bold = bold
    if italic is not None:
        f.italic = italic


def add_or_get_style(styles, name, style_type):
    try:
        return styles.add_style(name, style_type)
    except ValueError:
        return styles[name]


def add_pbdr(style, edges_xml):
    ppr = style.element.get_or_add_pPr()
    old = ppr.find(qn("w:pBdr"))
    if old is not None:
        ppr.remove(old)
    ppr.append(parse_xml(f"<w:pBdr {nsdecls('w')}>{edges_xml}</w:pBdr>"))


def add_shading(style, fill):
    ppr = style.element.get_or_add_pPr()
    old = ppr.find(qn("w:shd"))
    if old is not None:
        ppr.remove(old)
    ppr.append(parse_xml(f'<w:shd {nsdecls("w")} w:val="clear" w:fill="{fill}"/>'))


def remove_paragraph_border(style):
    ppr = style.element.get_or_add_pPr()
    old = ppr.find(qn("w:pBdr"))
    if old is not None:
        ppr.remove(old)


def add_box_styles(doc):
    styles = doc.styles

    doc_kind = add_or_get_style(styles, "DocKind", WD_STYLE_TYPE.PARAGRAPH)
    doc_kind.base_style = styles["Normal"]
    doc_kind.quick_style = True
    set_font(doc_kind, SANS, size=8.5, color=rgb(WPGRAY))
    doc_kind.font.small_caps = True
    doc_kind.paragraph_format.space_before = Pt(0)
    doc_kind.paragraph_format.space_after = Pt(4)

    key_box = add_or_get_style(styles, "KeyBox", WD_STYLE_TYPE.PARAGRAPH)
    key_box.base_style = styles["Normal"]
    key_box.quick_style = True
    set_font(key_box, SERIF, size=9.5)
    key_box.paragraph_format.space_before = Pt(6)
    key_box.paragraph_format.space_after = Pt(10)
    key_box.paragraph_format.line_spacing = 1.0

    method_box = add_or_get_style(styles, "MethodBox", WD_STYLE_TYPE.PARAGRAPH)
    method_box.base_style = styles["Normal"]
    method_box.quick_style = True
    set_font(method_box, SERIF, size=9)
    method_box.paragraph_format.space_before = Pt(10)
    method_box.paragraph_format.space_after = Pt(4)
    method_box.paragraph_format.line_spacing = 1.0

    try:
        set_font(styles["Verbatim Char"], MONO, size=8)
    except KeyError:
        pass


def main(out_path: str) -> None:
    with tempfile.TemporaryDirectory() as td:
        base = Path(td) / "base.docx"
        data = subprocess.run(
            ["pandoc", "--print-default-data-file", "reference.docx"],
            check=True,
            capture_output=True,
        ).stdout
        base.write_bytes(data)
        doc = Document(str(base))

        st = doc.styles
        plan = {
            "Normal": dict(name=SERIF, size=10.5),
            "Body Text": dict(name=SERIF, size=10.5),
            "First Paragraph": dict(name=SERIF, size=10.5),
            "Title": dict(name=SANS, size=26, color=rgb(WPBLUE), bold=True),
            "Subtitle": dict(name=SANS, size=13, color=rgb(WPGRAY), bold=False),
            "Author": dict(name=SANS, size=11, color=rgb(WPGRAY)),
            "Date": dict(name=SANS, size=10, color=rgb(WPGRAY)),
            "Heading 1": dict(name=SANS, size=14, color=rgb(WPBLUE), bold=True),
            "Heading 2": dict(name=SANS, size=12, color=rgb(WPBLUE), bold=True),
            "Heading 3": dict(name=SANS, size=11, color=rgb(WPBLUE), bold=True),
            "Heading 4": dict(name=SANS, size=10.5, color=rgb(WPGRAY), bold=True, italic=False),
            "Caption": dict(name=SANS, size=9, color=rgb(WPGRAY)),
            "Image Caption": dict(name=SANS, size=9, color=rgb(WPGRAY)),
            "Table Caption": dict(name=SANS, size=9, color=rgb(WPGRAY)),
            "Block Text": dict(name=SERIF, size=10, color=rgb(WPGRAY), italic=False),
            "Bibliography": dict(name=SERIF, size=9.5),
            "Footnote Text": dict(name=SERIF, size=9),
        }
        for sname, kw in plan.items():
            try:
                set_font(st[sname], **kw)
            except KeyError:
                print(f"  (style {sname} is absent from the Pandoc base, skipping)")

        for name, before, after in (
            ("Normal", 0, 4),
            ("Body Text", 0, 4),
            ("First Paragraph", 0, 4),
            ("Title", 2, 4),
            ("Subtitle", 0, 2),
            ("Date", 0, 12),
            ("Heading 1", 8, 3),
            ("Heading 2", 6, 2),
            ("Heading 3", 8, 4),
            ("Block Text", 0, 4),
        ):
            try:
                style = st[name]
            except KeyError:
                continue
            style.paragraph_format.space_before = Pt(before)
            style.paragraph_format.space_after = Pt(after)
            style.paragraph_format.line_spacing = 1.0

        try:
            st["Title"].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
            remove_paragraph_border(st["Title"])
        except KeyError:
            pass
        try:
            add_pbdr(st["Date"], f'<w:bottom w:val="single" w:sz="6" w:space="6" w:color="{WPRULE.lstrip("#")}"/>')
        except KeyError:
            pass

        add_box_styles(doc)

        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        doc.save(out_path)
        print(f"reference.docx written: {out_path}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "reference.docx")
