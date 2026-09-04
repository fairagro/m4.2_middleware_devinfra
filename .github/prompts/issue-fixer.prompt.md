---
description: "Triage and fix a GitHub issue (explore → draft PR → local implement; no auto fix commits)"
---

# issue-fixer

Triage and fix a GitHub issue following `.agents/skills/issue-fixer/SKILL.md`:

- Explore Feature/Refactoring (and wait for lock-in) before branch/PR
- Create one empty bootstrap commit on a clean tree, push it, open a **draft** PR with `Fixes #<issue_number>`
- Implement only in the working tree — do **not** auto-commit or auto-push fix commits
- Split deferred work via create-issue (`sub-of` vs `linked`)

Do not mark the PR ready. The empty bootstrap push is allowed; fix pushes are not unless the user asks.
