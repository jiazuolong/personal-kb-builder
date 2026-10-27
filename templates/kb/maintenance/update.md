# Update and review

Keep the KB trustworthy by making every change traceable.

## Adding a source

1. Put the raw file where it already lives. Do not copy it into the KB.
2. Run:

   ```bash
   python <skill>/scripts/scan.py --root <data-root> --out catalog
   ```

   This rewrites `catalog/sources.jsonl` and `catalog/coverage.json`. It never reads file contents.

3. Read the relevant part of the source in place.
4. Add an evidence section in `catalog/evidence.md`:

   ```markdown
   ## E003

   **Short title**

   Summary. One to three sentences.

   - source: `<absolute path>`
   - locator: `page 8 / paragraph 4 / function parse()`
   - kind: `document-reported`
   - limitation: `unverified; single source`
   - reviewed_at: `2026-10-27`
   ```

5. Link the E-ID from the relevant project/topic card.
6. Run `python <skill>/scripts/check.py --kb .`.

## Re-review

- Re-review when the source changes, when the user corrects a fact, or before quoting the claim in something external.
- Update `reviewed_at`; if the summary changed, note it in the card change log.
- If the source disappeared, keep the record but change `limitation` to `source-missing` and tell the user; do not pretend it is still verifiable.
- Never keep two contradictory "current" statements. Replace the old one.

## What belongs where

| You have… | Put it in… |
|---|---|
| A new file on disk | re-run `scan.py`; no manual entry needed |
| A claim with a source | `catalog/evidence.md` |
| A project status update | the project card |
| A dated event | `timeline.md` if source-backed |
| An unknown that blocks progress | `open-questions.md` |
| A decision about the KB itself | this folder, dated |

## Privacy checks (before committing)

- No source files copied into the KB.
- No secrets, tokens, ID numbers, financial or medical details.
- Absolute paths are acceptable, but consider replacing the user name with `<user>` when sharing.
- `sources.jsonl` contains paths and metadata only, never contents.

## Checks

`scripts/check.py` validates: required files, unique E-IDs, required evidence fields, internal Markdown links, JSON files, and (optionally) that source paths still exist.

```bash
python <skill>/scripts/check.py --kb .
python <skill>/scripts/check.py --kb . --check-sources
```
