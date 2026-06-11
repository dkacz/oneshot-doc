# Preset: letter (formal letter, official or business letter)

## Header Parameters

```text
GEOMETRY_OPTIONS = top=25mm,bottom=25mm,left=25mm,right=25mm
FONTSIZE         = 11pt
LINESPREAD       = 1.08
PARSKIP          = 0.6em
SECNUMDEPTH      = 0
TITLE_SIZE       = LARGE
KIND_LABEL       = (empty or sender institution name)
```

Default page budget: 1-2. A letter does not use `KeyBox` or `MethodBox`; the running header appears only from page 2, with no header on page 1 when the layout requires it.

## Skeleton

1. **Address block**: place and date on the right; sender on the left; recipient below, right or left according to the contract convention. For DOCX, build or normalize this block with `assets/docx_postprocess.py --address-block`.
2. **Case reference / subject**: one line (in Polish "Dotyczy: ...", in English "Re: ..."), functioning as the title; no large title block, the YAML `title` field stays empty, and the address block is laid out in LaTeX for PDF.
3. **Salutation** according to the contract register.
4. **Body**: first paragraph says what the letter concerns and what the sender expects; the middle carries the rationale; the last paragraph repeats the expectation with deadline.
5. **Closing formula and signature**: name, surname, function; attachments listed below the signature.

## Style and Visual Rules

- Formal register without antique stiffness; prefer direct contemporary formulas over ornate archaic ones.
- One letter, one matter; side issues are out of scope.
- No figures, boxes, or bibliography; footnotes only when the contract requires a legal basis in a footnote.
- The expectation always has a deadline and response mode if the contract knows them.
- Paragraphs have 3-6 sentences, left alignment with default LaTeX justification.

## Polish Addendum

- Subject line: "Dotyczy: ...".
- Register example: "zwracam się z prośbą" instead of "uprzejmie proszę o łaskawe".
- Closing formula: "Z poważaniem", name and function below, attachments listed under "Załączniki:".
