# Preset: memo (decision memo, internal memo)

## Header Parameters

```text
GEOMETRY_OPTIONS = top=20mm,bottom=20mm,left=24mm,right=24mm
FONTSIZE         = 10pt
LINESPREAD       = 1.0
PARSKIP          = 0.3em
SECNUMDEPTH      = 0
TITLE_SIZE       = LARGE
KIND_LABEL       = Memo  (or the contract label, in the document language)
```

Default page budget: 2. A decision maker reads it in two minutes; anything beyond that belongs in an appendix.

## Skeleton

1. **Recommendation box** (`KeyBox`): one declarative recommendation sentence plus decision deadline if one exists.
2. **Context**: at most one paragraph, only what is needed to understand the decision.
3. **Options**: two to three options, each in two or three sentences with cost and risk; the recommended option is marked directly.
4. **Recommendation rationale**: one paragraph, strongest argument first.
5. **Risks and safeguards**: compact points, each risk with a response.
6. **Next steps**: who, what, by when.

DOCX rule: the recommendation `KeyBox` must be a Pandoc `custom-style` block and must pass through `assets/docx_postprocess.py --boxes-to-tables`. Do not use a block quote or paragraph border as the DOCX fallback.

## Style and Visual Rules

- Short sentences, active verbs, no ornament.
- Figures are normally absent; if the contract wants one, it is a small unnumbered conceptual graphic.
- An options table is allowed instead of prose options if the contract prefers it (columns: option, cost, risk, recommendation).
- Dates are absolute (15 July 2026, not "in two weeks"); responsibilities are named if the contract knows them.
- Do not refer to materials the decision maker does not have at hand unless you summarize them in one sentence at the point of reference.

## Polish Addendum

- Typical Polish kind labels: "Notatka" or "Notatka decyzyjna".
- Dates in full Polish form (15 lipca 2026 r.), decimal comma in numbers.
