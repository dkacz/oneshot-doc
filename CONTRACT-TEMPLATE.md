# Document Contract Template

Copy this to `CONTRACT.md` in the document working directory and fill it during the interview. Mark any unresolved field as "to be settled"; the interview does not end while such a field exists. Do not add fields preemptively; remove sections the document type does not need, for example a letter usually has no figures.

```markdown
# Contract: <working title>

Family: <family slug> | Preset: <brief|report|memo|letter|summary>
Language: <pl|en> | Format: <pdf|docx|both> | Page budget: <N>
Theme: <think-tank|academic|minimal> | Accent override: <hex or none> | Base font size: <10-11pt>
Contract date: <YYYY-MM-DD>

## Thesis and Purpose

Main thesis (one declarative sentence): ...
Audience: ...
Purpose (what the reader should do or understand): ...

## Argument (in Order)

1. ...
2. ...

## Canonical Numbers

| Number | Meaning | Source (file, page/line) |
|---|---|---|
| ... | ... | ... |

Forbidden numbers (working, unapproved): ...

## Forbidden Zones

1. ...

## Tone and Voice

Register: ... | Temperature: ... | Person: ...
Stance toward institutions and literature: ...

## Structure

1. <section>: <what it carries>
2. ...

Opening box: <contents, number of paragraphs>
Method box / appendices: ...

## Figures

| No. | Purpose (one sentence) | Source data |
|---|---|---|
| 1 | ... | ... |

## Output and DOCX Layout

DOCX geometry: <A4,top=20,bottom=20,left=24,right=24>
Running header: <text or none>
Footer PAGE field: <yes/no; optional footer text>
Document kind label: <label or empty>
Address block JSON: <path or none, for letter>
Keep headings with next paragraph: <yes/no>

## Edges

Title: ... | Subtitle: ...
Author / institution / title-page date: ...
Bibliography: <style, what enters>
Caveats: ...

## Inherited from Family

Glossary: <version/date> | Decisions: <list of decision numbers that govern>
```
