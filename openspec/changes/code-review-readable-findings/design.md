## Context

Issue [#217](https://github.com/fairagro/m4.2_middleware_devinfra/issues/217). Wide findings tables crush Severity/Cost
on github.com. `/review-fixer` extracts via `extract_code_review_findings` (Markdown table + `path` column). Lock-in:
**A2** numbered blocks (no `###`), **B2** dual layout (blocks + compact table), **C2** legacy table-only still parses.

## Goals / Non-Goals

**Goals:**

- Readable GitHub COMMENT bodies at laptop width
- Preserve triage fields; keep review-fixer extraction via table
- Document dual layout in skill + docs; tests for dual + legacy

**Non-Goals:**

- HTML `<table>` / images
- Dropping the machine table (user chose B2, not B1-only)
- Rewriting review-fixer triage UX

## Decisions

1. **Human layout (A2):** after the marker + short verdict, each finding is:

   ```markdown
   1. **Short title**
   - **Severity:** Medium · **Cost:** cheap · **Goal:** Correctness
   - **Path:** `path/to/file.py` (`symbol`)
   - **Note:** …
   ```

2. **Machine table (B2):** after the list, a compact table (same columns/order as today) under a heading such as
   `## Findings index`. Same rows as the numbered list. Agents MUST fill both; skill calls out the sync obligation.

3. **Parser (C2):** leave `extract_code_review_findings` table-based; add fixture covering dual body; keep existing
   table-only fixture green.

4. **Empty findings:** omit numbered list and omit table (or single “none” row — document one approach: omit both when
   empty).

## Risks / Trade-offs

- **Dual maintenance** — agents may drift blocks vs table; mitigate with explicit skill rule + example.
- Compact table may still look mediocre on GitHub — acceptable because primary scan is the numbered list.

## Open Questions

- (none)
