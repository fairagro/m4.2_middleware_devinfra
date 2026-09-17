## Why

Synced `docker/Dockerfile.product-app.base` builds a single primary PyInstaller `--onedir` binary. At least one product
(harvester) also needs a second `--onefile` binary (e.g. K8s liveness `healthcheck`) next to the main onedir tree, but
must not hand-edit the synced base — today it keeps a product-local Dockerfile/Bake fork. Issue
[#71](https://github.com/fairagro/m4.2_middleware_devinfra/issues/71) asks the shared base to express one optional
secondary binary generically.

## What Changes

- Extend `binary-builder` / `export-binaries` so an optional secondary PyInstaller binary can land under `/dist` via
  build-args (empty secondary = current single-primary behavior)
- Document the secondary ARG surface and last-stage COPY expectations in `docs/ci.md` and update `docker/examples/`
- **Not in this change:** deleting harvester’s product-local healthcheck Dockerfile (product follow-up after sync);
  making the primary binary `--onefile`; supporting N secondaries

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `shared-product-app-dockerfile`: Require optional secondary binary ARGs on the shared base (name / import / onefile
  mode), no-op when unset, export under `/dist`, and document the contract for product Bake + last stage

## Impact

- Devinfra: `docker/Dockerfile.product-app.base`, `docs/ci.md`, `docker/examples/`, OpenSpec
  `shared-product-app-dockerfile`
- Products after sync: can pass secondary ARGs on the existing `*-base` Bake target and COPY from the same `export_bins`
  context; harvester can drop its healthcheck Dockerfile/Bake fork in a separate PR
