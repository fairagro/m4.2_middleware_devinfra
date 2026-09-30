## Why

`m42-ai issue-start` always opens draft PRs with a hardcoded `MVP scope: (fill in)` Summary. `/issue-fixer` now routes
almost every draft PR through that CLI, so real change summaries rarely appear. Agents previously wrote HEREDOC bodies
via `gh pr create`; the stub must not be the only path.

## What Changes

- `issue-start` builds a non-stub default PR body (issue context + short commit list vs base + `Fixes #<n>`).
- Optional `--body` / `--body-file` override for agent-crafted Summaries (and deferred links).
- Update `agent-ai-gh` `issue-start` contract, `/issue-fixer` skill/thin docs, and fixture tests.
- Keep no Cursor marketing footers; `pr-strip-footer` unchanged.

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `agent-ai-gh`: `issue-start` body rules (default + override; forbid fill-in-only stub).
- `issue-fixer`: draft-PR step documents passing a real Summary via `--body-file` (or relying on the CLI default).

## Impact

- Code: `scripts/ai/src/m42_ai/issue.py`, CLI args, `scripts/ai/tests/`.
- Docs/skills: issue-fixer `SKILL.md`, `docs/issue-fixer.md`, `scripts/ai/README.md` as needed.
- Specs: deltas above.
