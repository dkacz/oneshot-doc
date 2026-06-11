# Framing Decision Register Format (`decisions/`)

Decisions live in the family `decisions/` directory and are numbered sequentially: `0001-slug.md`, `0002-slug.md`. Create the directory lazily when the first decision appears. A new number is the highest existing number plus one.

## Template

```markdown
# <Short decision title>

<One to three sentences: the context, what was decided, and why.>
```

One paragraph is enough. The value lies in recording THAT the decision was made and WHY. Optional status (`active | superseded by 000N`), considered variants, and consequences are allowed only when they add real value.

## Triple Test (All Three Must Hold)

1. **Hard to reverse.** Changing the decision later has a cost, for example the document already circulates or the family tone is already recognizable.
2. **Surprising without context.** A future reader of the family will ask "why this way?"
3. **Result of a real tradeoff.** There were real variants and one was chosen for concrete reasons.

If any test is missing, do not record a decision. An easily reversible decision will simply be reversed; nobody will ask about an obvious "why"; and a choice without variants is not a choice.

## Decisions That Typically Pass

- Family forbidden zones: what documents never do and toward whom.
- Interpretive frame, for example immanent critique instead of a values dispute.
- Family title and subtitle conventions.
- Deliberate deviations from the obvious path, for example no section numbering in briefs despite numbered reports.
- Constraints invisible in the document text, for example a ban on citing works outside a closed canon.

Read all decisions at the start of each new family document and treat them as part of the contract that is not renegotiated.
