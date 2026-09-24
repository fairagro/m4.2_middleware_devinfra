## Context

See proposal.md — Why. Skill already teaches dual layout; github.com still renders the Findings index table poorly.
`extract_code_review_findings` today only reads the Markdown table. Main `code-review` / `agent-ai-gh` specs still
require a path table (in-flight `code-review-readable-findings` dual-layout delta not fully reflected as “table
optional”).

## Goals / Non-Goals

**Goals:**

- Numbered findings only in new reports; no Findings index table
- Parser: numbered Path bullets first; legacy table fallback
- Skill, thin command, docs, tests, specs aligned
- Supersede / drop conflicting in-flight dual-table change artifacts if still open

**Non-Goals:**

- HTML `<table>` / font-size restyles
- Changing Copilot suppressed-comment extraction
- Re-reviewing old PRs’ published bodies (legacy table parse is enough)

## Decisions

1. **Remove table (lock-in A)** — Not `<details>` hide; humans should not see a useless index.
2. **Parse numbered blocks** — Match skill template: after `N. **Title**`, collect bullets until next `N.` or heading;
   require a Path bullet with backtick path (strip optional ``(`symbol`)`` suffix like today’s table parser).
3. **Legacy table fallback** — If no numbered Path findings, keep existing table parse for old reviews.
4. **Prefer numbered when both present** — Or table-only if no numbered paths; if both, prefer numbered to match new SoT
   (tests cover both shapes).
5. **In-flight `code-review-readable-findings`** — Delete or leave abandoned when this change lands (do not archive dual
   table into main).

## Risks / Trade-offs

- [Risk] Agents still paste old dual template → Mitigation: skill/docs; parser still accepts table.
- [Risk] Path bullet wording drifts (`Path:` vs `**Path:**`) → Mitigation: document exact bullet shape; regex tolerant
  of bold/optional backticks.
- [Risk] Spec drift vs unarchived dual-layout change → Mitigation: explicit supersede task.

## Migration Plan

1. Specs + parser + skill/docs in one PR.
2. No data migration; old reviews keep working via table fallback.
3. Archive this change after merge; do not archive dual-table requirement.
