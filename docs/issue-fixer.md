# Issue-fixer conventions

Shared `/issue-fixer` triages a GitHub issue, explores Feature/Refactoring with the user, opens a draft PR from one
empty bootstrap commit, and implements locally without auto-committing fix commits. Canonical skill:
[`.agents/skills/issue-fixer/SKILL.md`](../.agents/skills/issue-fixer/SKILL.md).

Issue: [#15](https://github.com/fairagro/m4.2_middleware_devinfra/issues/15).

## Workflow (summary)

1. Fetch + triage (type, labels, done-when).
2. **Explore pause** for `Feature` / `Refactoring` (wait for lock-in / `go` / `skip explore`) — no branch/PR yet.
   `/opsx-explore` is **optional** (in-skill explore is enough).
3. **`/opsx-propose` is mandatory** before branch/PR/implement when the run will implement (see
   [`.cursor/skills/openspec-propose/SKILL.md`](../.cursor/skills/openspec-propose/SKILL.md)).
4. **Spec-review pause** — stop so you can review proposal / specs / design / tasks; continue only after your `go` /
   approval (or `/opsx-update` then `go`).
5. Prefer `uv run --project scripts/ai m42-ai issue-start --issue <n>` (branch + empty commit + draft PR with
   `Fixes #<n>`). Manual: branch `issue-<issue_number>-<slug>` from `main` → empty commit → `gh pr create --draft`.
6. Implement in the working tree (prefer `/opsx-apply`); user commits, pushes, marks ready.
7. Split only on logical blocks; deferred work via [`/create-issue`](create-issue.md) with relation:
   - **sub-of** — still part of this issue’s acceptance criteria (GitHub native sub-issue)
   - **linked** — distinct follow-up problem

## Auth

Same personal-token helpers as `/review-fixer` — see root README **Personal tokens** and `scripts/bin/gh`.
