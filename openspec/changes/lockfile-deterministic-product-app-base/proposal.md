## Why

Shared `docker/Dockerfile.product-app.base` installs built workspace wheels in `binary-builder` with
`uv pip install --system /tmp/wheels/*.whl`, which resolves transitive dependencies from the live package index instead
of `uv.lock`. Rebuilds of the same commit can therefore produce different dependency graphs, PyInstaller binaries, and
SBOMs. Products must not patch this synced file; the contract belongs in Devinfra (#73, flagged on harvester PR #181).

## What Changes

- Make `binary-builder` install runtime dependencies in a **lockfile-deterministic** way (Option A): bring `uv.lock` (+
  enough project/workspace metadata) into that stage, install locked deps with `uv sync --frozen` (or equivalent), then
  install the package-builder wheels with `--no-deps`.
- Keep `pyinstaller==${PYINSTALLER_VERSION}` pinned from `versions.env` (unchanged ARG contract).
- Document the install contract in `docs/ci.md` (and header comments on the base Dockerfile as needed).
- Update `shared-product-app-dockerfile` requirements to require lockfile-deterministic binary-builder installs.
- **BREAKING** for product Bake only if current images relied on unpinned transitive resolution (unlikely intentional);
  after sync, products should rebuild and smoke Bake.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `shared-product-app-dockerfile`: Require lockfile-deterministic dependency install in `binary-builder` (frozen lock /
  no live index resolve for wheel transitive deps); document the contract.

## Impact

- Devinfra: `docker/Dockerfile.product-app.base`, `docs/ci.md` (+ brief quality/docker notes if already pointing at the
  install path), OpenSpec `shared-product-app-dockerfile`.
- Product repos after sync: rebuild Bake targets; optional adopt/smoke follow-ups (no hand-edit of the base).
