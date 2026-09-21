# review-fixer PR-head hard gate

## Why

On a product `/review-fixer` run, `review-open` correctly fail-closed when the tree was dirty on another branch, but the
agent still improvised (stash → checkout → switch back). That breaks the “work on the PR head” contract. The skill
already mentions checkout; it needs a first hard gate and explicit stop/recovery rules so agents do not bypass a failed
checkout.

## What Changes

- Strengthen `.agents/skills/review-fixer/SKILL.md`: **first action** when a PR is known is always `m42-ai review-open`;
  no triage/fix until `current_branch` matches `head_ref`.
- On checkout failure: **stop immediately**, show the CLI error, do **not** stash/checkout around it, do **not**
  silently return to the previous branch after an empty open-work result.
- Document that dirty on the PR head is allowed (matches CLI). Thin docs/commands may get a one-line pointer.
- No CLI behavior change required (existing `ensure_pr_head` + tests stay).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `review-fixer`: PR-head checkout is a hard first gate with stop/no-improvise rules on failure

## Impact

- `.agents/skills/review-fixer/SKILL.md` (+ optional thin `docs/review-fixer.md` / command/prompt)
- Spec delta only; `scripts/ai` checkout plumbing unchanged
