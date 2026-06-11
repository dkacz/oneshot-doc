# Document Evaluation Rubric

Used by the Phase 4 critics and by the independent judge in skill tests. The total score is the MINIMUM of the three layers; the document is only as good as its weakest layer.

## Judge Materials

The judge receives: the contract or intent card, the source list with access to those sources, `NUMBERS.md`, the document text, screenshots of every PDF page, and DOCX screenshots after conversion if DOCX is in scope. The judge evaluates the result, not the effort; the judge does not read process reports from the producer before assigning scores.

## Layer 1: Substantive Fidelity to Sources

Check every number against `NUMBERS.md` and the sources, and check every claim against the sources and the contract. Check forbidden zones sentence by sentence.

- 10: every number and claim is supported, forbidden zones are untouched, source nuance (caveats, ranges, conditions) is preserved, and the contract thesis is clear without dilution.
- 9: support is complete, but one or two source nuances are flattened without changing meaning.
- 7-8: support is complete, but emphasis drifts from the contract, for example a side argument dominates.
- 5-6: at least one claim overinterprets a source, or a number is used outside the source conditions.
- 0-4: fabricated number, unsupported claim, or breached forbidden zone.

Hard cuts: any unsupported number or claim cuts Layer 1 to at most 6, which makes the total score lower than 9. A forbidden-zone breach cuts Layer 1 to at most 4.

## Layer 2: Language Style

Read as a demanding editor in the document language.

- 10: prose is fluent and rhythmic, every concept is defined before or at first use, sentences have subjects and verbs, there are no calques or cliches, tone matches the contract exactly, and sentence length is controlled.
- 9: one or two sentences need smoothing, with no substantive style errors such as undefined jargon, calques, or cliches.
- 7-8: several places need editing; one instance of undefined jargon or uneven register between sections.
- 5-6: the style is readable, but tone drifts from the contract or the prose sounds like raw translation.
- 0-4: language errors, unintelligible sentences, or tone contradicts the contract.

Hard cuts: a long dash anywhere in the document cuts Layer 2 to at most 8. A term that contradicts the family glossary cuts it to at most 8. Metanarration, a reference to the production process (contract, brief, revision rounds), an AI-created codename not grounded in the audience's nomenclature, or defensive prose (arguing with comments, explaining forbidden zones, or explaining what the document does not contain) cuts Layer 2 to at most 7 under rules 16-17 in `assets/STYLE.md`; preset genre elements are not metanarration.

## Layer 3: Visual Quality

Inspect screenshots of every page at target size.

- 10: the document looks professionally typeset: coherent typography and palette, even spacing, figures readable without effort, boxes closed correctly, and no collisions, widows, orphans, or overflows; the page budget is met.
- 9: one minor cosmetic issue, for example slightly uneven spacing, with no defect visible in ordinary reading.
- 7-8: visible issues that do not block understanding: uneven spacing, a figure too small or too large, or a break that leaves a lone line.
- 5-6: a defect makes reading harder: text collision, clipped label, overflowing box, or broken bibliography layout.
- 0-4: the document looks untypeset: broken layout, unreadable figures, or fallback fonts.

Hard cuts: exceeding the page budget cuts Layer 3 to at most 7. A label collision in a figure or a clipped element cuts it to at most 6.

## One-Shot and Three-Shot Protocol

**One-shot.** The first render shown by the producer is evaluated, with no corrections after scoring. The result is the minimum of the three layers plus a list of findings with addresses (page, section, sentence).

**Three-shot.** After the one-shot score, the judge acts as the operator and writes the annotations they would place on the PDF: concrete, anchored in document locations, and not phrased as ready-made replacement sentences. The producer implements them, and the judge scores again. There are at most two annotation rounds; the version after the second round (the third render) must reach 10/10 in all three layers, otherwise the case fails three-shot.

**Judge report.** A table of layer scores and the minimum, a list of blocking and cosmetic findings with addresses, a one-shot verdict (score), and a three-shot verdict (10/10 or failure with reason). The judge does not propose skill changes; post-battery failure analysis handles that.
