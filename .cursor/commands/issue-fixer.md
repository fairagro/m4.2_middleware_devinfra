---
name: "/issue-fixer"
id: "issue-fixer"
category: "Workflow"
description: "Triage and fix a GitHub issue (explore → opsx-propose → spec review → draft PR → implement)"
---

# issue-fixer

Triage and fix a GitHub issue: explore Feature/Refactoring with the user first, **always** run `/opsx-propose`, **pause
for spec review**, then open a **draft** PR from one empty bootstrap commit, then implement locally. Do **not**
auto-commit or auto-push fix commits.

**Input:** Issue number or URL.

**Steps**

1. Read and follow `.agents/skills/issue-fixer/SKILL.md`.
2. For `Feature` / `Refactoring`: explore and wait for lock-in (or `skip explore`) **before** any branch/commit/PR.
   `/opsx-explore` is **optional**.
3. **Required:** `/opsx-propose` (`.cursor/skills/openspec-propose/SKILL.md`) before branch/PR/implement whenever this
   run will implement. Do not skip when `openspec/` exists; if `openspec/` is missing, stop.
4. **Pause** after propose: wait for the user to review specs and say `go` / approve (or `/opsx-update` then `go`). Do
   not branch/PR/implement during that pause.
5. Allowed GitHub write before fixes: one empty commit (`Start issue #<issue_number>` on a clean tree) +
   `gh pr create --draft` with `Fixes #<issue_number>` in the body (or `m42-ai issue-start`). Do not mark the PR ready.
   Do not leave `Made with Cursor` (or similar) footers in the PR body — strip if injected.
6. Deferred splits via `/create-issue` (`relation: sub-of` for acceptance-criteria slices; `linked` for distinct
   follow-ups).
7. If `GH_TOKEN` is missing and there is no TTY, ask the user to run `source ./scripts/set-dev-tokens.sh` in a terminal
   and wait — do not paste tokens into chat.
