## Why

Per [#319](https://github.com/fairagro/m4.2_middleware_devinfra/issues/319), Cursor sparkle (and hand-typed subjects)
can emit `feat`/`fix` that pass commitlint’s type-enum while the staged index is only OpenSpec planning, archive+spec
sync, or tests — falsely bumping Release `version_bump: auto`. Agent handoff subjects help, but a path-aware commit-msg
gate is required so unread sparkle clicks cannot minor/patch-bump unnoticed (#320).

## What Changes

- Add a fleet `scripts/commit-path-check.sh` (or equivalent) that classifies staged paths and the Conventional Commits
  type from the commit message file
- Wire it as a **commit-msg** pre-commit hook alongside commitlint
- Reject `feat`/`fix` for OpenSpec-planning-only, archive/spec-sync-without-shipped-paths, and test-only indexes;
  optionally reject `docs(openspec): archive…` in favour of `chore(openspec)`
- Document in `docs/quality.md`; add fixtures; allowlist the script for product sync
- Does **not** replace `/issue-fixer` / `/review-fixer` handoff Suggested commit messages

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `shared-quality-tooling`: commit-stage MUST path-check Conventional Commits types against staged paths (in addition to
  commitlint type-enum)

## Impact

- Devinfra + synced products (`.pre-commit-config.yaml`, new script, `docs/quality.md`, sync allowlist)
- Contributors using sparkle / hand commits; Renovate `deps:` and empty/merge edge cases must remain allowed
- Related: #319 (decision), #321 (agent handoff already shipped separately)
