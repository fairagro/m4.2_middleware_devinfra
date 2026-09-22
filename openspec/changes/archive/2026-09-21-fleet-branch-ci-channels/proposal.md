## Why

Issue-fixer and humans often use `issue-<n>-…` branches. Shared `reusable-build` only mints RC versions on `feature/*`,
so Pre Release from an issue branch looks like a final `X.Y.Z` and can collide with a later release. Prefix `feature/`
also collides with the GitHub Feature issue type (a Bug should not require a “feature” branch). We need fleet branch
**channels** that encode CI intent, keep the issue number in the name, and align `/issue-fixer` + plumbing.

## What Changes

- **BREAKING:** RC / pre-release version suffix in `reusable-build` applies only to `build/*` (hard cut — no `feature/*`
  alias). Helm pre-release fails closed unless the ref is `build/*`.
- Document fleet channels: `build/`, `ci/`, `docs/`, `chore/` (prefix = CI channel; fine job selection stays on path
  filters). Issue work uses `{channel}/issue-<n>-<slug>`.
- `/issue-fixer` and `m42-ai issue-branch` / `issue-start` create channel-prefixed branches (`build` default; `docs` /
  `ci` when scope is clear).
- Update synced principles / CI docs that still describe `feature/*` as the work branch convention.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `reusable-ci-workflows`: pre-release version pattern gated on `build/*` instead of `feature/*`
- `issue-fixer`: issue branch naming uses CI channels; skill picks channel from scope
- `agent-ai-gh`: `issue-branch` / `issue-start` branch name shape includes channel prefix
- `global-principles`: shared trunk-based branch table uses CI channels (`build`/`ci`/`docs`/`chore`), not `feature/*`

## Impact

- `.github/workflows/reusable-build.yml`, `docs/ci.md`, `openspec/principles.global.md`
- `.agents/skills/issue-fixer/**`, thin issue-fixer docs/commands/prompts
- `scripts/ai` (`issue-branch` / `issue-start` CLI + tests)
- Product callers that still use `feature/*` for Pre Release must rename to `build/*` (hard cut)
