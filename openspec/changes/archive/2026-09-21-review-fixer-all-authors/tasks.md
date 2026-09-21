## 1. Plumbing

- [x] 1.1 Stop filtering unresolved threads by `is_ai_author` in `shape_review_open`; keep AI heuristics for reviews /
      suppressed; verify tests include human open thread + suppressed Copilot
- [x] 1.2 Pack `/code-review` COMMENT bodies (`<!-- m42-ai:code-review -->` + findings table) into summary_only;
      skip them as triage replies; `code-review-report-write` auto-prefixes the marker; tests for human-login
      code-review + answered/unanswered
- [x] 1.3 Update `scripts/ai/README.md` / CLI help wording for open work

## 2. Skill / docs

- [x] 2.1 Update `.agents/skills/review-fixer/SKILL.md` (any-author threads + Copilot + code-review summary)
- [x] 2.2 Update `.agents/skills/code-review/SKILL.md` Output shape (marker + table) and relationship table
- [x] 2.3 Update thin review-fixer / code-review docs/commands/prompts
- [x] 2.4 `openspec validate review-fixer-all-authors --strict` passes
