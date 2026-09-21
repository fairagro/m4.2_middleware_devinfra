# review-fixer PR-head hard gate

## Why

On a product `/review-fixer` run, `review-open` correctly fail-closed when the tree was dirty on another branch, but the
agent still improvised (stash → checkout → switch back). That breaks the “work on the PR head” contract. Gate semantics
belong in plumbing so agents only need to honor `ok` / `pr_head_ok` / `agent_action`.

## What Changes

- CLI `review-open`: structured gate failures (`error_code`, `pr_head_ok`, `agent_action: stop`) and success `ok` /
  `pr_head_ok`.
- Skill / thin docs: first action remains `review-open`; on failure trust CLI JSON and stop — no stash/improvise rules
  invented in the agent.
- Tests for structured dirty-wrong-branch JSON; existing checkout tests stay green.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `agent-ai-gh`: `review-open` PR-head gate emits structured stop JSON
- `review-fixer`: skill treats CLI `pr_head_ok` / `agent_action` as the hard gate

## Impact

- `scripts/ai` (`review.py`, `cli.py`, tests, README)
- `.agents/skills/review-fixer/SKILL.md` (+ thin docs/commands/prompts)
