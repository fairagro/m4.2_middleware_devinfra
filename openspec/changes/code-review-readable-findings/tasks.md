## 1. Skill and docs

- [x] 1.1 Update `.agents/skills/code-review/SKILL.md` Output shape + relationship wording (numbered blocks + Findings
      index table; marker unchanged)
- [x] 1.2 Update `docs/code-review.md` and any prompts that hard-code the old table-only shape

## 2. Tests / fixtures

- [x] 2.1 Add dual-layout fixture body; assert `extract_code_review_findings` still returns rows from the table
- [x] 2.2 Keep legacy table-only fixture green (C2)

## 3. Validate

- [x] 3.1 `uv run pytest scripts/ai/tests/test_review_filter.py` (focused)
- [x] 3.2 `openspec validate code-review-readable-findings --strict`
