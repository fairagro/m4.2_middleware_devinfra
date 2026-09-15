## Context

See proposal.md — Why. Today `review-open` only GraphQL-shapes open AI work (`scripts/ai/src/m42_ai/review.py`).
`issue-branch` already refuse-on-dirty + checkout (`issue.py`). Option A (locked): fold PR-head ensure into
`review-open` so `/review-fixer` keeps a single first CLI call.

## Goals / Non-Goals

**Goals:**

- Fail-closed wrong-branch protection before agents edit for `fix`.
- Reuse `issue-branch` cleanliness semantics (dirty only blocks when current ≠ head).
- Structured JSON still usable for triage; include head branch for agent assert.

**Non-Goals:**

- Separate `review-checkout` command (Option B deferred).
- Changing reply/resolve, policy, or commit/push rules.
- Auto-stash / auto-commit of dirty work.
- Full fork remote setup beyond what `gh pr checkout` already does — fail closed if checkout cannot succeed.

## Decisions

1. **Checkout inside `review-open`, not a new subcommand** — matches issue preference and skill “start from
   review-open”. Alternative B rejected at explore lock-in.

2. **Resolve head via `gh pr view --json headRefName,…` (or equivalent) before/alongside GraphQL** — GraphQL query today
   omits head ref; keep GraphQL for review shaping; use a small `gh pr view` (or extend query) for head. Prefer
   `gh pr checkout <n>` when switching branches so fork/cross-repo cases get gh’s existing behavior; on failure emit
   error JSON and exit non-zero.

3. **Dirty rule** — If `git status --porcelain` non-empty **and** `branch --show-current` ≠ head ref → refuse (no
   checkout). If already on head (dirty or clean) → proceed. If clean and wrong branch → checkout then shape.

4. **JSON fields** — Add `head_ref` (PR head name) and `current_branch` (after ensure). Keep existing open-work keys
   unchanged.

5. **Skill/docs** — One short note: first step = `review-open`; do not `fix`-edit until success. No second CLI step.

6. **Tests** — Unit/integration with temp git repos + mocked `gh` for head resolution: happy checkout, dirty
   wrong-branch refuse, already-on-head dirty allowed. Shaping fixtures remain independent of checkout where possible
   (inject/skip ensure in pure shape tests).

## Risks / Trade-offs

- [Risk] `review-open` now has side effects (checkout) → Mitigation: document in README/skill; error JSON is explicit.
- [Risk] Cross-repo PRs fail checkout → Mitigation: fail closed; agent surfaces error (no silent main edits).
- [Trade-off] Coupling fetch + git vs dedicated command → Accepted (Option A).

## Migration Plan

Ship CLI + skill/docs together on the issue branch. Consumers sync `scripts/ai` + review-fixer skill on next product
sync. No data migration.
