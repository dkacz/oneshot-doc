# Preset: brief (policy brief, thematic brief)

## Header Parameters

```text
GEOMETRY_OPTIONS = top=21mm,bottom=21mm,left=24mm,right=24mm
FONTSIZE         = 10pt          (qmd YAML: fontsize)
LINESPREAD       = 1.0
PARSKIP          = 0.34em
SECNUMDEPTH      = 0
TITLE_SIZE       = Huge
KIND_LABEL       = Policy brief  (or the contract label)
```

Default page budget: 4 (the contract may change it). qmd YAML: `documentclass: scrartcl`, `pdf-engine: lualatex`, `fig-pos: "tb"`, `colorlinks: true`, Figure-name localization for non-English documents goes in `include-before-body` (see Polish Addendum).

## Skeleton

1. **Opening box** (`KeyBox`, title "At a glance" or the contract equivalent): two prose paragraphs in abstract style. The first says what was checked and on what basis; the second gives the result with numbers. No bullets that carry many claims at once.
2. **3-4 sections**, each with a heading that carries the section thesis, not a label ("What the data show: debt higher, not lower", not "Results").
3. **Conclusions** as 2-4 compact points with concrete addressees.
4. **Method box** (`MethodBox`) at the end: where the numbers come from and what their limits are.
5. **Bibliography** in two columns (`multicol`) in small type, only works cited in the text.

DOCX rule: `KeyBox` and `MethodBox` must be Pandoc `custom-style` blocks and must pass through `assets/docx_postprocess.py --boxes-to-tables`. If a box contains bullets, begin the box with a non-list title or lead paragraph so Pandoc emits the box marker before the list.

## Style and Visual Rules

- Every technical concept is defined at first use in one plain-language sentence.
- Logical bridge between sections: the last sentence of a section opens the next one.
- Maximum 2 numbered figures (55-70% width) plus optionally 1-2 small conceptual graphics without number or caption (LaTeX `center`, 40-80% width), so numbering stays clean.
- Figures are built with `palette.py`; one purpose per figure; labels use full words, with no abbreviations absent from the text.
- Numbers in text and figures must be identical in notation.
- The document must fit the budget without squeezing: if it misses by more than a few lines, cut content, not typography. Minor adjustments such as figure width or `vspace` around uncaptioned graphics are allowed.

## Polish Addendum

- Opening box title: "W skrócie".
- Add `\renewcommand{\figurename}{Wykres}` in `include-before-body`.
- Decimal comma in text and figures; thesis-heading example: "Co pokazują dane: dług wyżej, nie niżej".
