# Proposal: shared-git-hooks-lfs

## Why

Issue [#9](https://github.com/fairagro/m4.2_middleware_devinfra/issues/9): product repos need the same
version-controlled Git LFS hooks and a **pre-push** hook that runs LFS then the shared pre-commit **pre-push** stage
(pytest + container-structure-test from #7). Commit-stage install stays `pre-commit install`; only LFS-related hooks
live under `scripts/git-hooks/`.

Blockers #7 and #8 are closed. Primary reference: `m4.2_advanced_middleware_api` `scripts/setup-git-lfs.sh` +
`scripts/git-hooks/`.

## What Changes

- Add `scripts/setup-git-lfs.sh`: local `git lfs install`, copy hooks from `scripts/git-hooks/` into `.git/hooks/`.
- Add `scripts/git-hooks/`: `pre-push` (LFS then pre-commit `--hook-type=pre-push`), plus LFS `post-checkout`,
  `post-commit`, `post-merge`.
- Document install (postCreate / clone) and the commit-stage vs pre-push split; point CST/pytest at #7 runner and
  pre-push stages.
- Adapt the API pattern to Devinfra principles: **`uv` / Dev Container first** (no Homebrew auto-install); prefer
  `uv run pre-commit` when resolving the pre-push runner.

## Capabilities

### New Capabilities

- `shared-git-hooks-lfs`: Version-controlled Git LFS + pre-push quality hooks and installer for sync into product repos.

### Modified Capabilities

- `shared-quality-tooling`: Docs/install boundary — pre-push **git** hook install is provided by this change (no longer
  deferred solely to “issue #9” without an installer).

## Impact

- Consumers sync `scripts/setup-git-lfs.sh` and `scripts/git-hooks/`; run installer after clone / from postCreate (#10
  may wire the call).
- Requires `git-lfs` on PATH in the Dev Container (already common) or host; setup fails clearly if missing (no brew).
- Pre-push runs Docker-backed CST / pytest when those hooks are configured — same as manual
  `pre-commit run --hook-stage pre-push`.
