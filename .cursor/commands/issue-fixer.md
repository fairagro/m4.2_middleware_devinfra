---
name: "/issue-fixer"
id: "issue-fixer"
category: "Workflow"
description: "Triage and fix a GitHub issue (opsx-explore → branch→propose→pause → apply→pause → archive)"
---

# issue-fixer

Triage and fix a GitHub issue. When explore is required, use **`/opsx-explore`**. Then OpenSpec cadence: **create issue
branch → `/opsx-propose` → pause → draft PR + `/opsx-apply` → pause → `/opsx-archive`**. OpenSpec is **only** for this
skill (not `/review-fixer` / `/create-issue`). Do **not** auto-commit or auto-push fix commits.

**Input:** Issue number or URL.

**Steps**

1. Read and follow `.agents/skills/issue-fixer/SKILL.md`.
2. When explore is required (`Feature` / `Refactoring`, or unclear Bug/Security/Task / user asks): read and follow
   `.cursor/skills/openspec-explore/SKILL.md` (`/opsx-explore`). Wait for lock-in / `go` / `skip explore`.
3. Create `issue-<n>-<slug>` from `main`, then **`/opsx-propose`**, then **pause** for spec review (user may commit).
   Wait for `go`.
4. On continue: ensure **draft** PR + **`/opsx-apply`** → **pause** for the user to review/commit/push. No
   `Made with Cursor` footers in the PR body.
5. On continue: **`/opsx-archive`**.
6. Deferred splits via `/create-issue` (`relation: sub-of` / `linked`) — create-issue itself does **not** run OpenSpec.
7. If `GH_TOKEN` is missing and there is no TTY, ask the user to run `source ./scripts/set-dev-tokens.sh` in a terminal
   and wait — do not paste tokens into chat.
