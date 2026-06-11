# Interview Protocol (Grill)

The interview must produce a contract from which the document can be written without a single guess. Question the operator rigorously, branch by branch, until you share a concrete understanding of every decision that affects the document.

## Conduct Rules

1. **One question at a time** (in harness mode: rounds of three to six questions). Ask the next question only after the previous answer, because each answer opens and closes branches.
2. **Every question includes a recommendation.** For each question, give your recommended answer with one sentence of reasoning. The operator can accept the recommendation with one word.
3. **Sources instead of questions.** If the answer can be established from the specified sources, check the sources and do not ask. Instead of "what is the value of X", say "source Y gives X as Z, so I am putting it into the contract".
4. **Confront numbers and facts with sources.** When the operator gives a number or fact, check it against the sources before recording it. Point out any mismatch immediately, including what the source says and where.
5. **Confront terms with the family glossary.** When the operator uses a term that conflicts with the glossary, flag it immediately and ask which term governs. When a term is vague or overloaded, propose a canonical term.
6. **Test edge cases.** Test theses and formulations against concrete situations: how a hostile reader would quote one sentence, what a journalist would do with it, and how it sounds out of context. Record the result in forbidden zones or tone.
7. **Write continuously.** Every settled point goes into `CONTRACT.md` when it is decided, not in a batch at the end. Terminology decisions go straight into the family glossary.
8. **Inherit, do not re-ask.** Do not ask about things already settled by the family glossary or decision register. At the start, tell the operator in two sentences what you inherit so they can object.
9. **Exhaust the decision tree.** The seven branches below are trunks, not a ceiling. Every operator answer can open a sub-branch (a new decision, dependency, or conflict with an earlier settlement), and you go down it immediately before returning to the trunk. Resolve dependencies in the order in which they block further questions; do not leave "we will come back to that". The interview may end only when no branch or sub-branch is open and you cannot ask a question whose answer would change the document.

## Branches to Traverse (Recommended Order)

1. **Frame.** Document type and preset, audience, purpose (what the reader should do or understand after reading), language, page budget, output format.
2. **Thesis and argument.** One main thesis as a declarative sentence. Three to seven argument points in the operator's order. The strongest evidence and whether the sources support it.
3. **Canonical numbers.** The list of numbers the document may cite, each with a source address. Numbers that must not be used, for example unapproved or working values. This branch is mostly your source work, not questions.
4. **Forbidden zones.** Claims we do not make. Tones we do not use. Entities we do not attack or praise. Rhetorical moves outside scope. Ask directly: "what must this document not do under any circumstances?"
5. **Tone and voice.** Register (expert, journalistic, official), emotional temperature, stance toward literature and institutions, first or third person.
6. **Structure and figures.** Sections in order, what the opening box carries, how many figures and the purpose of each, what goes into a method box or appendix.
7. **Edges.** Title and subtitle (propose two to three variants), date and labels, bibliography (style and scope), legal or institutional caveats.

Close a branch only when its contract field is concrete. "Somewhat balanced" does not close tone; "expert, cool, no irony, critique of mechanism rather than persons" does.

## When the Interview Is Finished

The interview ends when `CONTRACT.md` has no "to be settled" field, no branch or sub-branch of the decision tree is open (rule 9), and you can answer "yes" to three control questions: can I point to the source of every number I plan to write; do I know what the document must not do; can I write the first and last sections without guessing. At the end, show the full contract to the operator for one-word approval.
