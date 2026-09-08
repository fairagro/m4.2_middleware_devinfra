# Shared product app Dockerfile base + Bake (issue #36)

## Why

Product app Dockerfiles (API / sql-to-arc / harvester) share the same `package-builder → binary-builder → runtime`
skeleton but diverge in pins, PyInstaller, and runtime finishing. Issue #28 deferred this work; #36 must land a **shared
base** here so sync (#13) can converge products without overwriting product-specific last stages.

## What Changes

- Add synced **`docker/Dockerfile.product-app.base`** (C2): `package-builder`, `binary-builder` (ARGs for real
  differences), and `export-binaries` for Bake contexts
- Document **product-local last stage** + Bake layout; ship example last-stage + `docker-bake.hcl` stubs (not used by
  Devinfra CST)
- **BREAKING:** Switch `reusable-build.yml` (and `reusable-release.yml` build path) to **Buildx Bake only** (A4,
  B2-strict) — no monolith `file: docker/Dockerfile.<component>` fallback. Callers must adopt base + last + bake before
  bumping the workflow ref
- Update `docs/ci.md` / `docs/quality.md` (and Wave/sync expectations): sync base; do not sync last stage; cutover
  warning for strict Bake
- Out of scope: migrating the three product Dockerfiles in this PR (adoption via #13 / product Wave C)

## Capabilities

### New Capabilities

- `shared-product-app-dockerfile`: Shared product-app Dockerfile base with ARGs, export stage, last-stage/Bake/sync
  contract and structure expectations for the three products

### Modified Capabilities

- `reusable-ci-workflows`: Build (and release rebuild) MUST use Bake with base + last-stage contexts instead of a single
  monolith `docker/Dockerfile.<component>` file path

## Impact

- New paths under `docker/` in Devinfra; docs; `.github/workflows/reusable-build.yml` and `reusable-release.yml`
- Product repos: cannot consume the new workflow ref until they split Dockerfiles and add Bake (document on Wave C /
  #13)
- Defaults for remaining explore items: **R=yes** (release with Bake), **P** = `docker/Dockerfile.product-app.base`,
  **M=mixed** (builder extras in base; runtime finishing in last), **S**=docs + Wave C cutover note
