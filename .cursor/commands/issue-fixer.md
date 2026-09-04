---
name: "/issue-fixer"
id: "issue-fixer"
category: "Workflow"
description: "Triage and fix a GitHub issue (explore → draft PR from empty commit → local implement)"
---

# issue-fixer

Triage and fix a GitHub issue: explore Feature/Refactoring with the user first, then open a **draft** PR from one empty
bootstrap commit, then implement locally. Do **not** auto-commit or auto-push fix commits.

**Input:** Issue number or URL.

**Steps**

1. Read and follow `.agents/skills/issue-fixer/SKILL.md`.
2. For `Feature` / `Refactoring`: explore and wait for lock-in (or `skip explore`) **before** any branch/commit/PR.
3. Allowed GitHub write before fixes: one empty commit (`Start issue #<issue_number>` on a clean tree) +
   `gh pr create --draft` with `Fixes #<issue_number>` in the body. Do not mark the PR ready.
4. Deferred splits via `/create-issue` (`relation: sub-of` for acceptance-criteria slices; `linked` for distinct
   follow-ups).
5. If `GH_TOKEN` is missing and there is no TTY, ask the user to run `source ./scripts/set-dev-tokens.sh` in a terminal
   and wait — do not paste tokens into chat.
