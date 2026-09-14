# Portable m42-ai / consumer-safe skills & principles — Proposal

## Why

Synced fixer skills and thin docs still show bare `uv run m42-ai …`, which fails in product checkouts where `scripts/ai`
is intentionally **not** a root workspace member. Consumer Wave A adopt PRs (and Copilot) keep flagging that gap after
#45/#46. Products must not patch synced files locally — SoT is Devinfra.

## What Changes

- First-party fixer skills (`issue-fixer`, `create-issue`, `review-fixer`) and matching thin docs prefer
  `uv run --project scripts/ai m42-ai …` (portable). Brief note that bare `uv run m42-ai` is only OK when `scripts/ai`
  is a root workspace member (Devinfra).
- Confirm `scripts/ai` keeps pytest available for `uv run --project scripts/ai pytest` (already via `default-groups`;
  touch only if still broken for a clean consumer checkout).
- Keep `docs/conventions.md` skill links (file is now on the sync allowlist).
- Soften `openspec/principles.global.md` Code Quality to portable wording (shared fragments when present / project
  config; `docs/quality.md` when synced) so consumers are not told they hard-require missing files.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `agent-ai-gh`: Synced skills/docs prefer portable `--project scripts/ai` invoke; `scripts/ai` pytest remains runnable
  via `--project` in consumers
- `issue-fixer`: Documented CLI examples use portable `--project scripts/ai` form
- `create-issue`: Documented CLI examples use portable `--project scripts/ai` form
- `review-fixer`: Documented CLI examples use portable `--project scripts/ai` form
- `global-principles`: Code Quality wording stays accurate for all consumers (no hard-require of missing product files)

## Impact

- `.agents/skills/{issue-fixer,create-issue,review-fixer}/SKILL.md`
- Thin docs: `docs/issue-fixer.md`, `docs/create-issue.md`, `docs/review-fixer.md` (and entrypoints only if they embed
  bare `uv run m42-ai`)
- `openspec/principles.global.md` Code Quality section
- Possibly `scripts/ai/pyproject.toml` / lock only if pytest still missing for consumers
- Specs under `openspec/specs/` for the capabilities above (delta → archive)
- No CLI behavior change; no product-local patches; sync picks this up on next adopt
