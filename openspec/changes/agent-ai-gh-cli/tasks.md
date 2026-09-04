## 1. CLI package

- [x] 1.1 Add `scripts/ai/` pyproject, package `m42_ai`, console script `m42-ai`, README
- [x] 1.2 Implement `gh`/`git` subprocess helpers (PATH wrappers)
- [x] 1.3 Implement `review-open` shaping + fetch
- [x] 1.4 Implement `review-reply` / `review-resolve`
- [x] 1.5 Implement `issue-create` (labels, type, parent fallback rules)
- [x] 1.6 Implement `issue-start` (clean tree, empty commit, draft PR)

## 2. Tests

- [x] 2.1 Add GraphQL fixture(s) and unit tests for filter/shape/slugify
- [x] 2.2 Run `uv run --project scripts/ai --extra dev pytest` (fixtures only)

## 3. Skill / docs wiring

- [x] 3.1 Point `/review-fixer` at `m42-ai review-open` / reply / resolve
- [x] 3.2 Point `/create-issue` at `m42-ai issue-create`
- [x] 3.3 Point `/issue-fixer` at `m42-ai issue-start` + thin docs/README
- [x] 3.4 Make `/opsx-propose` **required** in issue-fixer skill, Cursor command, Copilot prompt, docs

## 4. OpenSpec / verify

- [x] 4.1 Propose change `agent-ai-gh-cli` (this change)
- [ ] 4.2 Sync or archive related `extract-issue-fixer` leftovers if still open after merge
- [ ] 4.3 Sanity: `m42-ai --help`; format/lint touched Markdown if needed
