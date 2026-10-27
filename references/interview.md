# Interview protocol

The interview is the part that turns "here are my files" into a KB that matches the user's real goals. Keep it short and structured.

## Budget

- Maximum 3 rounds before the first artifact.
- Maximum 3 questions per round, 8 questions total.
- Every question is a choice with 2–4 options when possible; free text only for paths and names.
- If the user says "just do it", use the recommended defaults, state them, and continue.

## Round 1 — Goal, location, privacy (always)

| # | Question | Options (recommended first) |
|---|---|---|
| 1 | What should this KB mainly help with? | Research / papers (Recommended when the data looks academic) · Work projects · Learning notes · Life archive · Mixed |
| 2 | Where does the data live? | A few local folders · An external drive / D: · A cloud-synced folder · Only files I upload now |
| 3 | What must be excluded? | Nothing / include everything (Recommended) · Some private folders · Only certain file types · Only selected files |

For question 2, accept a typed path; give examples instead of pressure. Validate the path exists before scanning; if not, ask again once, then continue with what is available.

## Round 2 — Shape of the data

| # | Question | Options |
|---|---|---|
| 4 | Roughly how much data? | Under 1 GB · 1–20 GB · 20–200 GB · More than 200 GB (sample only) |
| 5 | What kind of files dominate? | Documents / PDFs (Recommended) · Notes and Markdown · Code and notebooks · Spreadsheets · Images and scans · Mixed |
| 6 | Do you already use a tool? | None (Recommended) · Obsidian · Zotero · Notion / other export · Bookmarks browser |

## Round 3 — Output preferences

| # | Question | Options |
|---|---|---|
| 7 | What language should the KB be written in? | Same as this chat (Recommended) · Chinese · English · Bilingual |
| 8 | How much detail? | Lightweight index (Recommended) · Evidence-grade with locators · Both: index now, evidence later |

After round 3, stop asking and produce the skeleton. Further questions belong inside the KB as `open-questions.md`.

## Question-tool patterns

In DSH, call `ask_user_question` with a `questions` array; each question has `id`, `header`, `question`, optional `options` (each with `label` and `description`), and `multi_select`. In other agents, use the equivalent structured question tool; otherwise ask the same questions in prose.

Guidelines:

- Put `(Recommended)` in the first option's label; describe the trade-off in one sentence.
- Never mix two decisions into one question.
- Do not ask for facts you can derive from the inventory (counts, file types, years).
- Do not ask for passwords, tokens, API keys, or identity numbers.
- Ask about exclusions before scanning, not after.
- When the user chooses "only files I upload now", treat uploads as read-only samples; record their origin and do not copy them into the KB.

## What to do with answers

Record the answers in `profile/profile.md` as a short table plus a "decisions taken" list. Use them to:

- choose the schema variant (`references/schema.md`),
- set scan scope and exclusions,
- decide the depth of evidence records,
- choose the KB language.

## Anti-patterns

- A 12-question onboarding form. The user abandons it.
- Asking "what do you want?" with no options.
- Scanning first and asking later.
- Treating inferred persona facts as user-confirmed.
- Asking the same question twice in different words.
