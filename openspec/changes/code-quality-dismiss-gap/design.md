## Context

See proposal.md — Why. Lock-in **B**: docs/skill honesty + `review-open` finding enrichment; no dismiss write path.

## Goals / Non-Goals

**Goals:**

- Agents and humans see that resolving a CQ bot thread does not clear Code Quality finding `state`.
- `review-open` JSON carries correlatable `code_quality_finding` (or equivalent) on CQ threads when the REST API returns
  findings.
- Phase-1 output / skill rules forbid claiming “open work clear” when linked findings remain `open`.

**Non-Goals:**

- Implementing dismiss/write against an undocumented API.
- Changing GitHub quality-gate configuration.
- Fixing product PRs that currently have open CQ findings (spot-check only).

## Decisions

1. **Enrichment in `review-open`, not a separate command** — one fetch already gates checkout; findings attach there so
   fixer always sees them.
2. **Soft-fail API** — missing preview header, 404, or empty list MUST NOT fail `review-open`; omit enrichment.
3. **Correlation heuristic** — match primarily on `location.path` + rule title/id / message overlap with the first
   review comment; prefer exact path + rule id when present; leave `code_quality_finding: null` when ambiguous.
4. **Author detection** — treat first-comment author login `github-code-quality` (and documented aliases if any) as CQ
   bot threads eligible for enrichment.
5. **Skill Phase 1** — for CQ threads (or any thread with linked finding `state: open`), after `dismiss`/`fix` thread
   actions, print explicit “manual Dismiss finding required” (or “re-scan after real fix”) and count Remaining risk /
   open work as not clear solely from `resolveReviewThread`.

## Risks / Trade-offs

- [Risk] Correlation false positives/negatives → Mitigation: null when ambiguous; document heuristic; fixtures.
- [Risk] API preview / permissions differ per repo → Mitigation: soft-fail; still document manual dismiss.
- [Risk] Agents ignore the new warning → Mitigation: normative skill MUST language + docs example in Phase-1 footer.
