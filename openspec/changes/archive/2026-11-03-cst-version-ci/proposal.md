## Why

CI Container Structure Tests use `plexsystems/container-structure-test-action`, which bundles an opaque CST binary and
exposes no version input. Fleet `versions.env` already pins `CST_VERSION` for the Dev Container; that pin never reaches
CI, so local `cst` and Check can diverge (#331).

## What Changes

- Add a shared install helper (git-cliff pattern) that installs the official release binary from caller `CST_VERSION`
- Replace the plexsystems Action in `reusable-check.yml` with install + `container-structure-test test …`
- Fail closed if `CST_VERSION` is missing/empty; document CI pin independence in `docs/ci.md`; allowlist the script for
  sync

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `reusable-ci-workflows`: Container Structure Tests MUST use caller `versions.env` `CST_VERSION`

## Impact

- `scripts/install-cst.sh` (new), `.github/workflows/reusable-check.yml`, `docs/ci.md`, sync allowlist
- OpenSpec `reusable-ci-workflows` (on archive)
