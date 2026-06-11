# oneshot-doc

`oneshot-doc` is a Claude Code skill for one-shot production of polished PDF and DOCX documents from supplied source material. It uses an internal interview, contract, gates, and critics loop so the operator receives a send-ready document rather than an exposed draft.

The skill is for Claude Code users who want reproducible production of briefs, reports, decision memos, letters, and analytical summaries. The skill protocol is in English. Output documents can be written in Polish or English, depending on the contract.

## Installation

Clone this repository into the Claude skills directory:

```bash
git clone <repo-url> ~/.claude/skills/oneshot-doc
```

Then start Claude Code normally. The skill activates when the operator asks for a finished document from source materials.

## Dependencies

System tools:

- `quarto`
- A LaTeX engine with `fontspec` support, such as XeLaTeX or LuaLaTeX
- `pandoc` on `PATH` for `pandoc --print-default-data-file reference.docx`
- LibreOffice `soffice` for DOCX preview conversion
- Poppler tools: `pdffonts`, `pdftotext`, `pdftoppm`

Python:

- Python 3
- `python-docx`, imported as `docx`
- `matplotlib`
- `pypdf`

The bundled scripts otherwise use the Python standard library. There is no `pdfplumber` import in the current scripts.

## Fonts

Install Source Sans 3 and Source Serif 4. Both are distributed by Adobe Fonts under the SIL Open Font License.

The font resolver checks, in order:

1. `ONESHOT_FONTS_DIR`
2. `~/.fonts/source-sans` and `~/.fonts/source-serif`
3. System-installed families discoverable as `Source Sans 3` and `Source Serif 4` through Matplotlib

`ONESHOT_FONTS_DIR` may point to a directory containing `source-sans/` and `source-serif/` subdirectories, or to a directory containing both families' `.otf` or `.ttf` files directly.

## Workflow

Phase 0 creates or loads the document family memory: glossary, decisions, and archived contracts.

Phase 1 runs the interview and writes a complete `CONTRACT.md`. The interview stops only when all fields are settled.

Phase 2 produces figures, the Quarto source, the LaTeX header, `NUMBERS.md`, and the first PDF/DOCX render cycle through the canonical runner.

Phase 3 runs programmatic gates for page budget, PDF/DOCX parity, dashes, metanarration, number licensing, bibliography hygiene, embedded fonts, figure label diacritics, screenshots, and DOCX preview.

Phase 4 runs three independent critics: substantive, style, and visual. Blocking findings return to Phase 3.

Phase 5 delivers file paths, page counts, a short description, a contract-compliance report, and updates the family glossary and decision register.

## Hard Rules

- The skill uses its own bundled resources only: `assets/`, `checks/`, and the protocol files beside `SKILL.md`.
- Every factual claim and number must be supported by sources in the contract.
- Long dashes are not allowed in source or rendered output.
- Forbidden zones in the contract are binding.
- The skill writes files to disk but does not send, publish, or share them.
- Renders are shown only after programmatic gates and critic review pass, unless the result is an explicit blocker report.

## What makes it one-shot

The draft and revision cycle happens inside the skill before the operator sees the result. The canonical runner checks the rendered PDF and DOCX, including DOCX parity against PDF page starts. The gates scan for metanarration and defensive prose, verify number licensing, inspect fonts and figures, and prepare screenshots for visual review. Three critics then independently check substance, style, and layout before delivery.
