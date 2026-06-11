# Preset: raport (analytical report, working paper, longer analysis)

## Header Parameters

```text
GEOMETRY_OPTIONS = top=24mm,bottom=24mm,left=26mm,right=26mm
FONTSIZE         = 10.5pt
LINESPREAD       = 1.04
PARSKIP          = 0.5em
SECNUMDEPTH      = 1
TITLE_SIZE       = Huge
KIND_LABEL       = Raport  (or the contract label)
```

Default page budget: 8-16 (set by the contract). YAML as in `brief`; for documents above 10 pages add `toc: true`, `toc-depth: 2`, and a Polish `toc-title:` when the document language is Polish.

## Skeleton

1. **Executive summary** (`KeyBox`): three to five paragraphs or compact points; result and significance, not a prose table of contents.
2. **Introduction**: problem, question, what the reader gets.
3. **Substantive sections** numbered, each closed with one conclusion sentence.
4. **Methodology** as a section or `MethodBox`, depending on audience; the contract decides.
5. **Conclusions and recommendations** separated: what follows from the data separately from what is proposed.
6. **Bibliography** single-column, full descriptions.

DOCX rule: `KeyBox` and `MethodBox` must be Pandoc `custom-style` blocks and must pass through `assets/docx_postprocess.py --boxes-to-tables`. If the executive summary uses compact points, start the box with a non-list title or lead paragraph so the postprocessor can wrap the whole list into one Word table cell.

## Style and Visual Rules

- Method concept introduction pattern: bold term, simple explanation first, then concrete example, notation last. Jargon is not used before explanation.
- Numbered figures with full captions (what is visible, data source); width 70-90%; tables use `booktabs`, no vertical lines.
- A section must not start with a figure or table; first comes a leading sentence.
- Running header: title shortened to at most 60 characters.
- Repeatability: every number in the report has an address in `NUMBERS.md`; result tables refer to source files in captions if the contract wants this.
