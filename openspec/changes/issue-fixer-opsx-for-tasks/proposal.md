# issue-fixer: OpenSpec for Task / Feature / Refactoring — Proposal

## Why

`/issue-fixer` currently forbids OpenSpec for every run. That fits Bug (and cheap Security) fixes, but Tasks and
Features that add durable behaviour or contracts get implemented with no change folder — agents follow the skill; humans
expected `/opsx-*` (e.g. sql_to_arc Git LFS overlay). Route those types through OpenSpec while keeping the fast path for
bugs.

## What Changes

- By org issue type: **Task**, **Feature**, and **Refactoring** require an embedded OpenSpec path (follow
  `openspec-propose` then `openspec-apply-change`, then after the draft PR **`openspec-archive-change` as the last
  `go`**). **Bug** and cheap **Security** stay no-OpenSpec unless the user asks. **Discussion** still does not implement
  by default.
- Keep in-skill explore (no required `/opsx-explore`). Propose artifacts are the locked plan.
- Keep branch `issue-<n>-<slug>` via `issue-branch` **before** propose. Draft PR still waits for real commits
  (`issue-start`); no auto-commit of fix commits; no empty bootstrap.
- Document `skip_specs: true` vs real delta specs (contract change → delta; docs/tooling-only with no capability change
  → skip_specs).
- `/review-fixer` and `/create-issue` stay off OpenSpec.
- Update skill, Cursor command, Copilot prompt, `docs/issue-fixer.md`, and the `issue-fixer` spec. Sync allowlist
  already covers the skill — products must not fork it.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `issue-fixer`: Replace the global “does not run OpenSpec” rule with type-routed OpenSpec (propose → apply → draft PR →
  archive as last `go` for Task/Feature/Refactoring; Bug/Security fast path unchanged)

## Impact

- `.agents/skills/issue-fixer/SKILL.md`, `.cursor/commands/issue-fixer.md`, `.github/prompts/issue-fixer.prompt.md`,
  `docs/issue-fixer.md`, README blurb, `openspec/specs/issue-fixer/spec.md`
- No CLI / `m42-ai` contract change; no OpenSpec CLI rewrite; no Wave A/B adopt-order change
- Consumer checkouts pick this up on next skill sync (#45)
