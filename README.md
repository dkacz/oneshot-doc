# oneshot-doc

`oneshot-doc` is a Claude Code skill for one-shot production of polished PDF and DOCX documents from supplied source material. It uses an internal interview, contract, gates, and critics loop so the operator receives a send-ready document rather than an exposed draft.

The skill is for Claude Code users who want reproducible production of briefs, reports, decision memos, letters, and analytical summaries (presets: brief, report, memo, letter, summary). The operator is led by the hand: the interview asks one question at a time with a recommendation, and after delivery the operator only says whether they are satisfied and what to change. The skill protocol is in English. Output documents can be written in Polish or English, depending on the contract.

## Visual themes

The look of the document is chosen in the interview, not hard-coded. The skill ships three named themes, each a fully tested code path (LaTeX header, figure palette, DOCX reference styles, DOCX postprocess colors):

- `think-tank` (default): sans headings, serif body, navy primary, brick accent, assertive title block.
- `academic`: serif typography, centered title block framed by thin rules, warm paper tones, maroon accent.
- `minimal`: sans throughout, near-black ink, generous whitespace, teal accent, no decorative rules.

Within a theme the contract may override the accent color and the base font size (10-11 pt). There is no free-form styling outside the named themes; that bound is what keeps the output predictable, because every theme passes the same render, gate, and parity pipeline before it ships. All themes use the same two font families, so the installation requirements do not change with the theme.

## Installation

The simplest path is to let your AI coding agent do the whole installation. Paste one line into Claude Code:

```text
Install the oneshot-doc skill following https://github.com/dkacz/oneshot-doc/blob/main/INSTALL.md
```

`INSTALL.md` walks the agent through cloning, dependency checks (`checks/check_env.py`), per-OS installs, and fonts, and ends with a verified environment.

Manual route: clone this repository into the Claude skills directory and install the dependencies below yourself.

```bash
git clone https://github.com/dkacz/oneshot-doc ~/.claude/skills/oneshot-doc
```

Then start Claude Code normally. The skill activates when the operator asks for a finished document from source materials.

Supported platforms: macOS and Linux. On Windows use WSL with Ubuntu and follow the Debian/Ubuntu steps inside WSL; native Windows is untested because the pipeline needs `soffice` and Poppler tools on PATH.

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

## Quick start on a clean system

macOS:

```bash
brew install quarto pandoc poppler
brew install --cask libreoffice
quarto install tinytex
pip3 install python-docx matplotlib pypdf
```

Debian/Ubuntu:

```bash
# Install Quarto from the .deb package at https://quarto.org/docs/get-started/
sudo apt install pandoc poppler-utils libreoffice texlive-xetex texlive-luatex
sudo apt install python3-docx python3-matplotlib python3-pypdf
```

Note on PEP 668: recent Homebrew and Debian/Ubuntu Pythons are externally managed, so a bare `pip3 install` fails with `externally-managed-environment`. On Debian/Ubuntu prefer the `apt` packages above. On macOS either run `pip3 install --break-system-packages python-docx matplotlib pypdf`, or create a virtual environment (`python3 -m venv ~/.venvs/oneshot-doc`) and make sure the skill's Python scripts run with that environment's interpreter.

Install Source Sans 3 and Source Serif 4 from Adobe Fonts under the SIL Open Font License:

```bash
mkdir -p ~/.fonts/source-sans ~/.fonts/source-serif
# Download from https://github.com/adobe-fonts/source-sans and https://github.com/adobe-fonts/source-serif
# Put Source Sans 3 font files in ~/.fonts/source-sans and Source Serif 4 font files in ~/.fonts/source-serif.
# Alternatively, set ONESHOT_FONTS_DIR to a directory containing source-sans/ and source-serif/.
python3 checks/check_env.py
```

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

Phase 2 produces figures, the Quarto source, the LaTeX header from the contract theme, `NUMBERS.md`, and the first PDF/DOCX render cycle through the canonical runner.

Phase 3 runs programmatic gates for page budget, PDF/DOCX parity, dashes, metanarration, number licensing, bibliography hygiene, embedded fonts, figure label diacritics, screenshots, and DOCX preview.

Phase 4 runs three independent critics: substantive, style, and visual. Blocking findings return to Phase 3.

Phase 5 delivers file paths, page counts, a short description, and a contract-compliance report, then collects the operator's verdict with guiding questions (substance, language, look, anything missing). Operator-requested changes go through the full cycle again; the operator never scores or applies a rubric. Once the operator is satisfied, the family glossary and decision register are updated.

## Hard Rules

- The skill uses its own bundled resources only: `assets/`, `checks/`, and the protocol files beside `SKILL.md`.
- Every factual claim and number must be supported by sources in the contract.
- Long dashes are not allowed in source or rendered output.
- Forbidden zones in the contract are binding.
- The skill writes files to disk but does not send, publish, or share them.
- Renders are shown only after programmatic gates and critic review pass, unless the result is an explicit blocker report.

## What makes it one-shot

The draft and revision cycle happens inside the skill before the operator sees the result. The canonical runner checks the rendered PDF and DOCX, including DOCX parity against PDF page starts. The gates scan for metanarration and defensive prose, verify number licensing, inspect fonts and figures, and prepare screenshots for visual review. Three critics then independently check substance, style, and layout before delivery.
