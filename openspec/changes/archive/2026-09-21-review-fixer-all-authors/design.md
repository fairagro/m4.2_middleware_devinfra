## Context

See proposal.md — Why. Lock-in #189: all unresolved threads + keep Copilot suppressed + triage `/code-review` COMMENT
reviews.

## Goals / Non-Goals

**Goals:** Any-author unresolved threads; Copilot suppressed packing unchanged; code-review reports in summary_only path
via stable marker + table extract.

**Non-Goals:** Inline comment threads from code-review (publish stays COMMENT body); changing triage policy.

## Decisions

1. Keep JSON key `unresolved_ai_threads` (compat); populate with all unresolved threads.
2. `is_ai_author` for bot logins; `is_code_review_report(body)` via `<!-- m42-ai:code-review -->`.
3. Finder reviews = AI author **or** code-review marker; `extract_code_review_findings` parses Markdown findings table
   rows into `summary_only_findings` (non-resolvable), same answered/open_summary selection as suppressed Copilot.
4. code-review skill Output shape MUST start with the marker and use a findings table with a `path` column.

## Risks / Trade-offs

- [Human nits in fixer runs] → Accepted.
- [Ad-hoc Markdown tables] → Marker required; without it, code-review body is ignored for summary packing.

## Migration Plan

Land Devinfra; products sync skill/CLI. Older code-review posts without the marker need a re-publish or paste triage.

## Open Questions

None.
