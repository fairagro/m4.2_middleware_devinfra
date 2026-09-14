## 1. Verify scripts/ai pytest

- [x] 1.1 Confirm `uv run --project scripts/ai pytest` collects/passes; fix `scripts/ai/pyproject.toml` / lock only if
      needed

## 2. Portable m42-ai in fixer skills

- [x] 2.1 Update `.agents/skills/issue-fixer/SKILL.md` examples to `uv run --project scripts/ai m42-ai …` (+ short
      Devinfra note)
- [x] 2.2 Update `.agents/skills/create-issue/SKILL.md` the same way
- [x] 2.3 Update `.agents/skills/review-fixer/SKILL.md` the same way

## 3. Thin docs / entrypoints

- [x] 3.1 Update `docs/issue-fixer.md`, `docs/create-issue.md`, `docs/review-fixer.md` where they embed bare
      `uv run m42-ai`
- [x] 3.2 Check Cursor commands / Copilot prompts; update only if they embed bare `uv run m42-ai`

## 4. Principles Code Quality

- [x] 4.1 Soften `openspec/principles.global.md` Code Quality to portable fragment / project-config wording

## 5. Format and validate

- [x] 5.1 Format only touched Markdown with Prettier; lint those paths;
      `openspec validate portable-m42-ai-consumer-docs --strict`
