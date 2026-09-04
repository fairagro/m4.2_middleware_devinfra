# Issue-fixer conventions

Shared `/issue-fixer` triages a GitHub issue, explores when needed, then runs the OpenSpec cadence and a draft PR from
one empty bootstrap commit, implementing locally without auto-committing fix commits. Canonical skill:
[`.agents/skills/issue-fixer/SKILL.md`](../.agents/skills/issue-fixer/SKILL.md).

Issue: [#15](https://github.com/fairagro/m4.2_middleware_devinfra/issues/15).

OpenSpec (`/opsx-*`) is **only** for `/issue-fixer` — not `/review-fixer` or `/create-issue`.

## Workflow (summary)

1. Fetch + triage (type, labels, done-when).
2. When explore is required (`Feature` / `Refactoring`, or Bug/Security/Task when criteria are unclear / user asks):
   **`/opsx-explore`** (no parallel in-skill explore). Wait for lock-in / `go` / `skip explore`.
3. **OpenSpec cadence** (mandatory when this run will implement):
   1. `/opsx-propose` → **pause** (review proposal / specs / design / tasks)
   2. On continue: draft PR (`m42-ai issue-start` or manual empty bootstrap) + `/opsx-apply` → **pause** (review /
      commit / push working tree)
   3. On continue: `/opsx-archive`
4. No `Made with Cursor` (or similar) footers in PR bodies — strip if injected.
5. Split only on logical blocks; deferred work via [`/create-issue`](create-issue.md) with relation:
   - **sub-of** — still part of this issue’s acceptance criteria (GitHub native sub-issue)
   - **linked** — distinct follow-up problem

## Auth

Same personal-token helpers as `/review-fixer` — see root README **Personal tokens** and `scripts/bin/gh`.
