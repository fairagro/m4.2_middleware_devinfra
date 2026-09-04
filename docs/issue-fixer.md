# Issue-fixer conventions

Shared `/issue-fixer` triages a GitHub issue, explores Feature/Refactoring with the user, opens a draft PR from one
empty bootstrap commit, and implements locally without auto-committing fix commits. Canonical skill:
[`.agents/skills/issue-fixer/SKILL.md`](../.agents/skills/issue-fixer/SKILL.md).

Issue: [#15](https://github.com/fairagro/m4.2_middleware_devinfra/issues/15).

## Workflow (summary)

1. Fetch + triage (type, labels, done-when).
2. **Explore pause** for `Feature` / `Refactoring` (wait for lock-in / `go` / `skip explore`) — no branch/PR yet.
3. Branch `issue-<n>-<slug>` from `main` → one empty commit `Start issue #<n>` on a clean tree → push →
   `gh pr create --draft` with `Fixes #<n>`.
4. Implement in the working tree; user commits, pushes, marks ready.
5. Split only on logical blocks; deferred work via [`/create-issue`](create-issue.md) with relation:
   - **sub-of** — still part of this issue’s acceptance criteria (GitHub native sub-issue)
   - **linked** — distinct follow-up problem

## Auth

Same personal-token helpers as `/review-fixer` — see root README **Personal tokens** and `scripts/bin/gh`.
