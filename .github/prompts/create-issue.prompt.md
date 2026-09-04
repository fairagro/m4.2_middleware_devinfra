---
description: "Create a GitHub issue from an AI finding with org issue type + triage labels"
---

# create-issue

Create a new GitHub issue from an AI finding or discussion request.

Follow `.agents/skills/create-issue/SKILL.md` to:

- choose exactly one org issue type (`Bug`, `Security`, `Feature`, `Task`, `Discussion`, `Refactoring`)
- attach triage labels (`severity:*`, `practicality:*`, `cost:*`)
- create missing allowlisted labels only (never free-text labels)

Use `docs/ai_review_policy.md` for severity / practicality / cost core definitions (issue extensions are in the skill).

Do not re-run `/review-fixer` triage. Do not commit or push unless asked.
