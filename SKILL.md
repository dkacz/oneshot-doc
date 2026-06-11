---
name: oneshot-doc
description: One-shot production of polished PDF and DOCX documents (brief, report, decision memo, letter, analytical summary) from specified sources. A rigorous interview creates the contract, the visual system runs as code, and internal QA gates plus critics bring the document to send-ready quality before the operator sees it. Use when the operator asks for a finished document from source materials.
---

# oneshot-doc: a finished document in one pass

This skill produces a document that is ready to send the first time it is shown. Iteration does not disappear; it moves inside the process. Rendering, measurement, correction, and re-rendering happen before the result is shown, not after.

The document is written in the language set by the contract, Polish or English. The skill protocol is in English; the output document follows the contract.

## Hard Rules (Always Apply)

0. **The skill is self-contained.** It works in any working directory, including an external repository with no helper files. Load every resource (style rules, presets, palette, header and DOCX templates, gates) only from this skill directory (`assets/`, `checks/`, and the protocol files beside `SKILL.md`), never from the project. If the project has files with similar names (`STYLE.md`, presets), ignore them; the skill resources are authoritative, and project requirements enter the document only through the contract. In an external repository, leave no traces outside the document working directory chosen at the start; the `.oneshot/` family memory also lives there.

1. **No fabrication.** Every number, fact, and claim in the document must be supported by the sources listed in the contract. Every number goes into `NUMBERS.md` with an exact source address (file, page, or line). If a fact is missing from the sources, it is missing from the document; raise the gap in the interview or mark it explicitly, never fill it with your own knowledge.
2. **No long dashes.** The characters `—` and `–` do not appear in the document source or in the rendered file. Write ranges with a normal hyphen (2028-2030). This applies in English as well.
3. **Forbidden zones are inviolable.** The contract lists claims, tones, and rhetorical moves the document must not make. If a forbidden zone blocks something important while writing, ask a question; never cross it quietly.
4. **Nothing is sent outside.** The skill ends with files on disk and a report. Sending, publishing, and sharing belong to the operator.
5. **The document must pass all gates before being shown.** Showing a render that has not passed programmatic gates and critic review is not allowed. If the gates still fail after repeated attempts, show a blocker report, not an unmarked draft.

## Workflow

### Phase 0: Document Family

Each document belongs to a family, for example "policy briefs for think tank X" or "decision memos for project Y". A family has a persistent memory directory:

```text
<project root>/.oneshot/<family-slug>/
├── GLOSSARY.md      # family terminology, format: GLOSSARY-FORMAT.md
├── decisions/       # framing decisions, format: DECISION-FORMAT.md
└── contracts/       # archived contracts for successive documents
```

At the start, locate the family directory. If it exists, read the glossary and every decision before asking the first question; the interview must not ask about things the family has already settled. If it does not exist, create it lazily when the first term or framing decision is settled.

### Phase 1: Interview and Contract

Run the interview according to `INTERVIEW.md`: rigorous, one question at a time, with a recommendation for every question, and with source confrontation instead of a question whenever the sources already answer it. Write the interview result continuously into `CONTRACT.md` using `CONTRACT-TEMPLATE.md`. The interview ends only when the contract has no "to be settled" fields.

The contract covers at least: document type and preset, visual theme and its parameters, main thesis, audience and purpose, language, page budget, canonical numbers with sources, forbidden zones, tone, section structure, figures and their intended purpose, output format (PDF, DOCX, or both), working title, and DOCX postprocess parameters.

### Visual Themes

The document's look is a contract decision, not an accident of the toolchain. The skill ships named themes, each a fully tested code path covering the LaTeX header, the figure palette, the DOCX reference styles, and the DOCX postprocess colors:

- `think-tank` (default): sans headings, serif body, navy primary with a brick accent, assertive title block with a heavy rule.
- `academic`: serif headings and body, centered title block framed by thin rules, warm paper tones with a maroon accent.
- `minimal`: sans throughout, near-black ink, generous whitespace, no decorative rules, teal accent.

The interview recommends a theme based on audience and genre; the operator picks. Two safe parameters may vary within a theme: an accent color override (hex) and the base font size (10-11 pt, set via `fontsize:` in the qmd YAML). There is no free-form styling outside themes: the QA gates guarantee mechanics for any input, but print-quality polish is guaranteed only on these tested paths. All themes use the same two font families, so no theme changes the installation requirements.

### Phase 2: Production

1. Build figures as separate Python scripts that use `assets/palette.py` for palette, fonts, and helper patterns; call `setup_fonts(theme=<contract theme>)` so figure colors match the document theme. Each figure has one purpose from the contract. After building, inspect every PNG for text collisions, clipped labels, and readability at target width.
2. Write the document as `.qmd` from the preset skeleton (`assets/presets/<type>.md`) with a LaTeX header generated from the contract theme's template `assets/themes/<theme>/header.tex` by replacing the double-brace fields. Take the replacement values (font directories and theme colors) from `assets/palette.py` via `font_template_values(<theme>)`. Write under the preset style rules and the family glossary.
3. Before Phase 3, run the mandatory self-check for rules 16-17 in `assets/STYLE.md`: read the whole text and remove every document self-reference (metanarration such as "ta notatka", "niniejszy dokument", "this report"), every reference to the production process (contract, production brief, interview, review rounds), and every defensive formulation (arguing with comments, explaining what the document does not contain, or defensively denying forbidden zones). The content speaks about its subject, not about itself.
4. Maintain `NUMBERS.md` in the document working directory: every number used in the text, its value, unit, and exact source address.
5. Run every complete production render and gate cycle through the canonical runner. The runner renders PDF, ensures `formatting/reference.docx` for DOCX when needed, renders DOCX, runs `assets/docx_postprocess.py` with the contract parameters, and runs `checks/qa_gates.py` once. Example:

```bash
python3 <skill-dir>/checks/run_pipeline.py \
  --qmd <file>.qmd \
  --budget <page budget> \
  --formats pdf,docx \
  --theme <theme from contract> \
  --postprocess-args '--geometry "A4,top=20,bottom=20,left=24,right=24" --running-header "<short header from contract>" --footer-page --doc-label "<document kind label>" --boxes-to-tables --keep-with-next' \
  --gates-args '<qa_gates.py extra args, for example --meta-allow "allowed phrase">' \
  --outdir qa
```

When the contract sets an accent override, add `--accent <hex>` next to `--theme`. The runner forwards the theme to the DOCX reference builder and the postprocess step, so both formats stay on the same theme without extra flags.

Manual assembly of `quarto render`, `assets/build_reference_docx.py`, `assets/docx_postprocess.py`, and `checks/qa_gates.py` is allowed only to debug one step. Every full cycle uses `checks/run_pipeline.py`.
6. Put all DOCX layout parameters from the contract into `--postprocess-args`. For the `letter` preset, add `--address-block <address-block.json>` there when the contract requires a sender/recipient block. The JSON may contain `city_date`, `sender_label`, `sender`, `recipient_label`, `recipient`, `recipient_align`, and `columns_twips`.
7. If the document uses `KeyBox` or `MethodBox`, the DOCX source must mark the box with `custom-style="KeyBox"` or `custom-style="MethodBox"` and `--postprocess-args` must include `--boxes-to-tables`. Do not emulate boxes in DOCX with block quotes, paragraph borders, manual rules, or document-specific scripts.
8. After the first runner cycle of both formats, align section page starts to the PDF by inserting explicit shared page breaks in the source. Do not leave critical section breaks to the LaTeX and Word automatic layout engines. A section heading must not remain at the bottom of a page; `--keep-with-next` helps, but section page breaks are explicit.

Paste this `page-break` pattern at every shared break point. Use `\clearpage` when pending figures or tables must flush; use `\newpage` only when no float flush is needed.

````markdown
::: {.content-visible when-format="pdf"}
```{=latex}
\clearpage
```
:::

::: {.content-visible when-format="docx"}
```{=openxml}
<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:r><w:br w:type="page"/></w:r></w:p>
```
:::
````

### Phase 3: Programmatic Gates

Run the same canonical `checks/run_pipeline.py` command from Phase 2 for every complete cycle; it invokes `checks/qa_gates.py` with the rendered files, page budget, `NUMBERS.md` when present, and any `--gates-args`. Manual `checks/qa_gates.py` calls are allowed only to debug one gate. The gates cover page budget for both PDF and DOCX, PDF/DOCX page-start parity (`docx_parity`), long dashes in source and rendered text, metanarration and defensive prose, number consistency against `NUMBERS.md`, bibliography hygiene, embedded fonts, Polish figure-label diacritics, and page screenshots for visual review. Fix every failure and run the runner again. The loop continues until all gates pass. Use `--parity-warn-only` inside `--gates-args` only when the operator has explicitly accepted different page breaks for that document.

Before Phase 4, if DOCX is in scope and the gates pass, review `qa/pages/` and the DOCX-preview page screenshots side by side, page by page. If `qa/docx_pages/` is absent, render it from the DOCX preview PDF first. Fix every discrepancy before running critics.

Parity checklist:

- The page break point is the same on every PDF and DOCX page.
- The title, label, and date use the same hierarchy, scale, and placement.
- Boxes are closed table frames, with bullets and text inside the frame.
- Tables keep the same columns and do not wrap labels differently.
- Figures and captions appear in the same relative places.
- Headers and footers are coherent across both formats.

### Phase 4: Critics

After clean gates, run three independent critics (separate agents, each receiving only what it needs for its layer):

- **Substantive critic** receives the contract, `NUMBERS.md`, sources, and document text. It checks every number and claim against the sources, checks forbidden zones sentence by sentence, explicitly checks rules 16-17 in `assets/STYLE.md`, and must not propose fixes that violate those rules. Its instruction is to disprove, not praise.
- **Style critic** receives the document text, preset style rules, `assets/STYLE.md`, and the family glossary. It looks for undefined jargon, sentences without a subject, calques, glossary violations, tone drift against the contract, and explicit violations of rules 16-17. It must not propose fixes that add metanarration, production-process references, or defensive prose.
- **Visual critic** receives screenshots of all pages from the gates, including DOCX screenshots when DOCX is in scope, plus preset visual rules. It looks for collisions, widows and orphans, bad breaks, overflowing boxes, unreadable figures, uneven spacing, and explicit visual or textual violations of rules 16-17. It must not propose labels or captions that violate those rules.

Write each critic's report to `qa/critics/` (`substantive_report.md`, `style_report.md`, `visual_report.md`). Classify every finding as blocking or cosmetic. Fix blocking findings and return to Phase 3. Fix cosmetic findings if they do not risk regression. The loop continues until no critic reports blockers.

### Phase 5: Delivery

Delivery precondition (hard): `qa/critics/` contains all three non-empty critic reports and no blocking finding remains unaddressed. If any report is missing, Phase 4 has not happened and delivery is forbidden; skipping the critics is a protocol violation even when every gate passes.

Show the operator: file paths (PDF and DOCX), page counts, three sentences on what the document does, a short contract-compliance report (thesis, forbidden zones, numbers, page budget), and a one-line critics summary (findings per critic, what was fixed). Then collect the operator's verdict with a few guiding questions, one dimension at a time, so feedback lands on actionable areas: are you satisfied with the substance (claims, numbers, emphasis)? with the language and tone? with the look of the PDF and the DOCX (layout, figures, boxes)? is anything missing or unnecessary? The operator answers in plain words; they are never asked to score, audit, or apply any rubric. If the operator requests changes, implement them as a new revision through the full runner cycle (Phases 2-4 as needed) and deliver again. When the operator is satisfied, update the family glossary and decision register with interview decisions that pass the triple test in `DECISION-FORMAT.md`, and archive the contract in `contracts/`.

## Roles

The skill leads the operator by the hand. In Phase 1 the interview always goes to the human operator, one question at a time, each with a recommendation, so the operator decides without having to design anything. After delivery the operator is not asked to score or audit the document; they simply say whether they are satisfied and what to change. The skill never assigns itself, a critic, or another model the judging role; critics are internal reviewers whose findings the producer must address before delivery, not evaluators of record.

## Document Working Directory

```text
<document directory>/
├── CONTRACT.md          # interview contract
├── NUMBERS.md           # source-backed number ledger
├── <name>.qmd           # document source
├── formatting/header.tex
├── figures/             # PNG files plus scripts
├── qa/                  # gate results, page screenshots, critic reports
└── <name>.pdf / .docx   # output
```

## Skill Files

- `INTERVIEW.md` - rigorous interview protocol
- `CONTRACT-TEMPLATE.md` - contract template
- `GLOSSARY-FORMAT.md`, `DECISION-FORMAT.md` - document-family memory
- `assets/` - palette and theme registry, per-theme LaTeX headers (`themes/<name>/header.tex`), presets, DOCX reference builder, DOCX postprocess module
- `checks/qa_gates.py` - programmatic gates
