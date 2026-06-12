# Installing oneshot-doc (guide for an AI coding agent)

This document is written for an AI coding agent (for example Claude Code) that has been asked to install the `oneshot-doc` skill. Execute the steps in order. Ask the user before every system-level installation. Do not stop at the first error; fix what can be fixed and re-verify.

## 1. Clone the skill

Target directory: `~/.claude/skills/oneshot-doc`.

If the target directory already exists, stop and ask the user whether to update it (`git pull` inside it) or leave it untouched. Otherwise:

```bash
git clone https://github.com/dkacz/oneshot-doc ~/.claude/skills/oneshot-doc
```

## 2. Check the environment

```bash
python3 ~/.claude/skills/oneshot-doc/checks/check_env.py
```

The script prints an OK/MISSING table for every dependency and exits 0 only when everything is present. If everything is OK, go to step 6.

## 3. Install missing system tools

Ask the user before each command.

macOS (Homebrew):

```bash
brew install quarto pandoc poppler
brew install --cask libreoffice
quarto install tinytex
```

Debian/Ubuntu:

```bash
# Quarto: install the .deb package from https://quarto.org/docs/get-started/
sudo apt install pandoc poppler-utils libreoffice texlive-xetex texlive-luatex
```

Windows (PowerShell; the toolchain is exercised in this repo's CI on `windows-latest`):

```powershell
winget install Quarto.Quarto JohnMacFarlane.Pandoc TheDocumentFoundation.LibreOffice
quarto install tinytex
```

Poppler on Windows: download the latest `Release-*.zip` from https://github.com/oschwartz10612/poppler-windows/releases, extract it, and add its `Library\bin` directory to PATH. LibreOffice and TinyTeX do not need to be on PATH; the skill's tool resolver checks their default install locations. WSL with Ubuntu remains a valid alternative (follow the Debian/Ubuntu steps inside WSL).

## 4. Install missing Python packages

Preferred on Debian/Ubuntu:

```bash
sudo apt install python3-docx python3-matplotlib python3-pypdf
```

Elsewhere:

```bash
python3 -m pip install python-docx matplotlib pypdf
```

If pip fails with `externally-managed-environment` (PEP 668), either add `--break-system-packages`, or create a virtual environment (`python3 -m venv ~/.venvs/oneshot-doc`) and make sure the skill's Python scripts run with that environment's interpreter.

## 5. Install the fonts

The skill needs Source Sans 3 and Source Serif 4 (Adobe Fonts, SIL Open Font License). Download the latest static OTF release of each family and place the `.otf` files in:

- `~/.fonts/source-sans` for Source Sans 3, from https://github.com/adobe-fonts/source-sans/releases
- `~/.fonts/source-serif` for Source Serif 4, from https://github.com/adobe-fonts/source-serif/releases

Alternatively set `ONESHOT_FONTS_DIR` to a directory that contains `source-sans/` and `source-serif/` subdirectories, or both families' font files directly.

## 6. Verify and report

Re-run the check from step 2 until every row is OK. Then tell the user, in their language, in about three sentences: the skill is installed; it activates when they ask for a finished document (brief, report, memo, letter, summary) from source materials; the skill interviews them one question at a time with a recommendation for each, and after delivery they only say whether they are satisfied and what to change.
