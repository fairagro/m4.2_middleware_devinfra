## Why

`/review-fixer` can apply local `fix` edits while the agent is still on `main` or an unrelated issue branch. Those
changes land in the wrong working tree and need manual rescue. Guarding checkout in `m42-ai` (fail-closed) prevents
silent wrong-branch edits.

## What Changes

- Extend `m42-ai review-open` so a PR-scoped open always resolves the PR head ref, ensures the local checkout matches it
  (fetch + checkout when needed), and returns the branch name in structured JSON.
- Refuse with clear error JSON when the working tree/index is dirty on a **different** branch than the PR head (dirty on
  the correct head remains allowed).
- Fail closed with clear JSON when the head cannot be checked out (e.g. unsupported cross-repo cases).
- Update `/review-fixer` skill + short docs: do not apply `fix` edits until `review-open` has established the PR head
  branch.
- Tests for happy path and dirty/wrong-branch refusal.

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `agent-ai-gh`: `review-open` MUST ensure PR head checkout before emitting open-work JSON (or fail closed).
- `review-fixer`: skill MUST treat PR-head checkout via `review-open` as a prerequisite before local `fix` edits.

## Impact

- `scripts/ai` (`review.py` / CLI / tests), `.agents/skills/review-fixer/SKILL.md`, `docs/review-fixer.md`,
  `scripts/ai/README.md`, OpenSpec deltas for `agent-ai-gh` and `review-fixer`.
- Synced consumers of review-fixer / `scripts/ai` pick this up on next product sync.
