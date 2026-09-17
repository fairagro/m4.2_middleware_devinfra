## Why

Product Feature-PR callers decide ad hoc whether to cancel in-progress runs and how to wire `detect-changes` + reusable
`skip`. Devinfra `docs/ci.md` shows only a partial jobs snippet, and shared `workflow_call` reusables lack complementary
concurrency. Fleet alignment belongs here ([#76](https://github.com/fairagro/m4.2_middleware_devinfra/issues/76)), not
only in one product PR (sql-to-arc Wave C discussion).

## What Changes

- Expand `docs/ci.md` Feature-PR into a **complete recommended caller**: workflow-level `concurrency`
  (`cancel-in-progress: true`), full `detect-changes` (`dorny/paths-filter`) with a suggested default path set, and
  existing `skip` / check `if:` wiring
- Document release / pre-release / Helm caller concurrency that **serializes** (`cancel-in-progress: false`); note
  `detect-changes` is Feature-PR-oriented
- Add complementary `concurrency` on outer Devinfra reusables (code-quality, build, check, release, helm-release,
  helm-pre-release, registry-retry) with repository + workflow identity + PR/ref groups
- Document that reusable concurrency does **not** replace caller-level full-pipeline cancel, and that `skip` /
  `detect-changes` remain **caller** responsibilities
- **Not in this change:** nested bake/push helper concurrency; product adoption PRs (sibling product issues)

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `reusable-ci-workflows`: Require complementary concurrency on the listed outer reusables; require docs for the
  complete Feature-PR caller snippet and release/Helm concurrency guidance (including the reusable-vs-caller and
  skip-ownership notes)

## Impact

- Devinfra: `docs/ci.md`, outer `.github/workflows/reusable-*.yml` listed above, OpenSpec `reusable-ci-workflows`
- Products after docs/`uses:` bump: can copy the recommended Feature-PR / release concurrency patterns; inherit basic
  reusable-level protection even with thin callers
