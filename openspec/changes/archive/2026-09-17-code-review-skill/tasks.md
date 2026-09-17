## 1. m42-ai plumbing

- [x] 1.1 Add `code-review-context` (base default `main`, optional `--pr`) returning JSON with base/head/paths/stats and
      verify unit tests with fixtures (no live GitHub)
- [x] 1.2 Add `code-review-report-write` writing `/tmp/code-review-*.md` and verify path + JSON in tests
- [x] 1.3 Add `code-review-publish` wrapping `gh pr review --comment` (local no-op without `--pr`; optional comment
      fallback) and verify mocked `gh` tests + CLI help entries
- [x] 1.4 Document the three commands in `scripts/ai/README.md` and verify the Commands table lists them

## 2. Skill and entrypoints

- [x] 2.1 Add `.agents/skills/code-review/SKILL.md` with locked goals, anti-duplication, Auth, m42-ai portable invoke,
      publish rules (COMMENT review vs `/tmp`) and verify it references `docs/ai_review_policy.md` and distinguishes
      `/review-fixer`
- [x] 2.2 Add `.cursor/commands/code-review.md` and `.github/prompts/code-review.prompt.md` pointing at the skill and
      verify they stay thin (no full checklist copy)
- [x] 2.3 Add `docs/code-review.md` and allowlist entries in `docs/synced-paths.yaml`; update README skill/docs index if
      other first-party skills are listed; verify allowlist paths exist on disk

## 3. Validate

- [x] 3.1 Run `uv run --project scripts/ai pytest` (or root equivalent) for new tests and verify green
- [x] 3.2 Run markdown format/lint on touched docs/skill Markdown and verify clean
- [x] 3.3 Run `openspec validate code-review-skill --strict` and verify it passes
