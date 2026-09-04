---
description: "Triage and fix a GitHub issue (opsx-explore → propose→pause → apply→pause → archive; no auto fix commits)"
---

# issue-fixer

Triage and fix a GitHub issue following `.agents/skills/issue-fixer/SKILL.md`:

- When explore is required: **`/opsx-explore`** (no parallel in-skill explore)
- OpenSpec cadence: **`/opsx-propose` → pause → `/opsx-apply` → pause → `/opsx-archive`**
- OpenSpec is **only** for `/issue-fixer` — not `/review-fixer` or `/create-issue`
- Draft PR from one empty bootstrap commit (`Fixes #<issue_number>`) — no `Made with Cursor` footers
- Implement only in the working tree — do **not** auto-commit or auto-push fix commits
- Split deferred work via create-issue (`sub-of` vs `linked`)

Do not mark the PR ready. The empty bootstrap push is allowed; fix pushes are not unless the user asks.
