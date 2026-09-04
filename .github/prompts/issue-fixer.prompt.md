---
description: "Triage and fix a GitHub issue (branch→propose→pause → apply→pause → archive; no auto fix commits)"
---

# issue-fixer

Triage and fix a GitHub issue following `.agents/skills/issue-fixer/SKILL.md`:

- When explore is required: **`/opsx-explore`** (no parallel in-skill explore)
- OpenSpec cadence: **create issue branch → `/opsx-propose` → pause → draft PR + `/opsx-apply` → pause →
  `/opsx-archive`**
- Create the branch **before** `/opsx-propose` so propose artifacts land on the issue branch and the user can commit
- OpenSpec is **only** for `/issue-fixer` — not `/review-fixer` or `/create-issue`
- Draft PR after propose confirmation (`Fixes #<issue_number>`) — no `Made with Cursor` footers
- Implement only in the working tree — do **not** auto-commit or auto-push fix commits
- Split deferred work via create-issue (`sub-of` vs `linked`)

Do not mark the PR ready. The empty bootstrap push is allowed; fix pushes are not unless the user asks.
