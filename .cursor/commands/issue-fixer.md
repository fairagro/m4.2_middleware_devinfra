---
name: "/issue-fixer"
id: "issue-fixer"
category: "Workflow"
description: "Triage and fix a GitHub issue (explore → propose→pause → apply→pause → archive)"
---

# issue-fixer

Triage and fix a GitHub issue. OpenSpec cadence: **`/opsx-propose` → pause → `/opsx-apply` → pause → `/opsx-archive`**.
`/opsx-explore` is optional. Do **not** auto-commit or auto-push fix commits.

**Input:** Issue number or URL.

**Steps**

1. Read and follow `.agents/skills/issue-fixer/SKILL.md`.
2. For `Feature` / `Refactoring`: explore and wait for lock-in (or `skip explore`) **before** any branch/commit/PR.
   `/opsx-explore` is **optional**.
3. **`/opsx-propose`** (`.cursor/skills/openspec-propose/SKILL.md`) → **pause** for spec review. Wait for `go`.
4. On continue: draft PR (`m42-ai issue-start` or empty bootstrap) + **`/opsx-apply`** → **pause** for the user to
   review/commit/push. No `Made with Cursor` footers in the PR body.
5. On continue: **`/opsx-archive`** (`.cursor/skills/openspec-archive-change/SKILL.md`).
6. Deferred splits via `/create-issue` (`relation: sub-of` for acceptance-criteria slices; `linked` for distinct
   follow-ups).
7. If `GH_TOKEN` is missing and there is no TTY, ask the user to run `source ./scripts/set-dev-tokens.sh` in a terminal
   and wait — do not paste tokens into chat.
