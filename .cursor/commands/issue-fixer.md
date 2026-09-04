---
name: "/issue-fixer"
id: "issue-fixer"
category: "Workflow"
description: "Triage and fix a GitHub issue (opsx-explore → propose→pause → apply→pause → archive)"
---

# issue-fixer

Triage and fix a GitHub issue. When explore is required, use **`/opsx-explore`** (not a built-in explore). Then OpenSpec
cadence: **`/opsx-propose` → pause → `/opsx-apply` → pause → `/opsx-archive`**. OpenSpec is **only** for this skill (not
`/review-fixer` / `/create-issue`). Do **not** auto-commit or auto-push fix commits.

**Input:** Issue number or URL.

**Steps**

1. Read and follow `.agents/skills/issue-fixer/SKILL.md`.
2. When explore is required (`Feature` / `Refactoring`, or unclear Bug/Security/Task / user asks): read and follow
   `.cursor/skills/openspec-explore/SKILL.md` (`/opsx-explore`). Wait for lock-in / `go` / `skip explore`.
3. **`/opsx-propose`** → **pause** for spec review. Wait for `go`.
4. On continue: draft PR (`m42-ai issue-start` or empty bootstrap) + **`/opsx-apply`** → **pause** for the user to
   review/commit/push. No `Made with Cursor` footers in the PR body.
5. On continue: **`/opsx-archive`**.
6. Deferred splits via `/create-issue` (`relation: sub-of` / `linked`) — create-issue itself does **not** run OpenSpec.
7. If `GH_TOKEN` is missing and there is no TTY, ask the user to run `source ./scripts/set-dev-tokens.sh` in a terminal
   and wait — do not paste tokens into chat.
