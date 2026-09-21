# shared-product-app-dockerfile Specification

## Purpose

Shared product-app Dockerfile base (package + binary builders with ARGs and an export stage) plus the documented
product-local last-stage and Buildx Bake sync contract so the three m4.2 products can converge without overwriting
runtime finishing.

## Requirements

### Requirement: Shared product-app Dockerfile base is present

The repository MUST provide `docker/Dockerfile.product-app.base` as the canonical shared multi-stage base for product
application images. The base MUST include stages equivalent to **package-builder**, **binary-builder**, and an
**export** stage that places build artifacts under a stable path (e.g. `/dist`) suitable for use as a Buildx Bake
additional context. Real differences across products (toolchain versions, packages to build, binary names, optional
builder extras such as extra compile `apk` packages) MUST be expressible via **ARG** (and documented defaults), not
hard-coded product names. The base MUST NOT encode product-specific runtime finishing (CMD/ENTRYPOINT, EXPOSE,
HEALTHCHECK, git system config, numeric UID policy, runtime-only apk installs) and MUST NOT download or install
product-only drivers (e.g. Microsoft ODBC for sql-to-arc) — those belong in the product-local last stage.

The **binary-builder** stage MUST install third-party / transitive runtime dependencies in a **lockfile-deterministic**
way from the product repo’s `uv.lock` (e.g. `uv sync --frozen` with documented flags). After locked dependencies are
present, workspace wheels produced by **package-builder** MUST be installed **without** resolving their `Requires-Dist`
against the live package index (e.g. `uv pip install --no-deps` on those wheels). The base MUST NOT use a bare
`uv pip install` of those wheels that re-resolves transitive dependencies from the index at image build time. Tooling
pins that are intentionally outside the lock (e.g. `pyinstaller==${PYINSTALLER_VERSION}` from `versions.env`) MAY remain
ARG-driven.

#### Scenario: Fresh clone has shared base

- **WHEN** a contributor clones the repository
- **THEN** `docker/Dockerfile.product-app.base` is present
- **AND** it defines package-builder, binary-builder, and export stages

#### Scenario: Base is parameterized

- **WHEN** a reader inspects the base Dockerfile and its docs
- **THEN** documented ARGs cover toolchain pins and product-varying build inputs (packages / binary identity / optional
  builder extras)
- **AND** runtime finishing directives are absent from the base (reserved for the product last stage)

#### Scenario: Binary-builder respects uv.lock for transitive deps

- **WHEN** a reader inspects the binary-builder install steps in `docker/Dockerfile.product-app.base`
- **THEN** transitive runtime dependencies are installed from `uv.lock` (frozen / locked sync or equivalent)
- **AND** package-builder wheels are installed without live-index resolution of their requires (e.g. `--no-deps`)
- **AND** the stage does not rely on bare `uv pip install /tmp/wheels/*.whl` alone for the dependency graph

### Requirement: Last-stage and Bake layout are documented

Documentation in this repository (at least `docs/ci.md` and `docs/quality.md` or a dedicated docker doc linked from
them) MUST describe: (1) the product-local last-stage file that consumes the export context; (2) a Buildx Bake file that
builds a base target then wires `contexts` so the last stage can `COPY --from` export artifacts; (3) sync boundaries for
#13 — base is synced, last stage and product Bake targets are not overwritten by sync; (4) structure expectations that
API, sql-to-arc, and harvester align to the same three-stage skeleton. The repository MUST ship non-production example
stubs (last stage and/or bake HCL) that illustrate the contract without requiring Devinfra to build a product app image
in CST.

#### Scenario: Contributor learns sync boundaries

- **WHEN** a contributor reads the docker/CI docs for product app images
- **THEN** they learn the shared base path and that the last stage stays product-local
- **AND** they learn Bake is required to compose base + last
- **AND** example stubs are available in-repo

### Requirement: Strict Bake cutover is documented

Documentation MUST state that reusable build/release workflows require the Bake + base + last-stage layout (**no**
monolith `docker/Dockerfile.<component>` fallback). Callers MUST NOT bump to a workflow ref that includes this change
until their product repo has adopted that layout. Product Wave C / sync (#13) issues are the adoption path.

#### Scenario: Caller reads cutover warning

- **WHEN** a product maintainer reads the reusable build docs after this change
- **THEN** they are warned that monolith single-file Dockerfiles are unsupported
- **AND** they are pointed at sync / Wave C adoption rather than a compatibility mode

### Requirement: Lockfile-deterministic binary-builder install is documented

Documentation in this repository (at least `docs/ci.md`) MUST state that `docker/Dockerfile.product-app.base`
`binary-builder` installs transitive dependencies from `uv.lock` and installs built workspace wheels without
re-resolving those dependencies from the live index, so product Bake rebuilds of the same lockfile are
dependency-reproducible (aside from intentionally ARG-pinned tools such as PyInstaller from `versions.env`).

#### Scenario: Contributor reads binary-builder install contract

- **WHEN** a contributor reads the product-app Bake / base Dockerfile docs
- **THEN** they learn binary-builder is lockfile-deterministic for transitive deps
- **AND** they learn wheels are installed without live-index transitive resolution

### Requirement: Optional secondary PyInstaller binary via build-args

The shared product-app base (`docker/Dockerfile.product-app.base`) MUST support building **at most one** optional
secondary PyInstaller binary in addition to the primary `--onedir` binary. When secondary identity build-args are
**unset or empty**, behavior MUST match the existing single-primary export (no secondary artifact under `/dist`).

When a secondary binary name is set, the base MUST:

- Resolve the secondary entry from a secondary import path (preferred) or an explicit secondary entry path after wheel
  install, using the same lockfile-deterministic environment as the primary build
- Build the secondary with PyInstaller `--onefile` by default when a secondary is requested, unless a documented
  build-arg opts into `--onedir` for the secondary
- Place both primary and secondary artifacts under the export stage’s stable `/dist` path so a product Bake last stage
  can consume them from the **same** export context (no second base Dockerfile required)

The base MUST NOT require products to fork or hand-edit `Dockerfile.product-app.base` to obtain a secondary binary. The
base MUST NOT encode product-specific HEALTHCHECK / CMD wiring for the secondary — that remains product-local last-stage
finishing.

#### Scenario: No secondary args — single primary only

- **WHEN** a Bake/base build omits secondary binary identity args (or sets them empty)
- **THEN** `export-binaries` contains the primary onedir tree under `/dist` as today
- **AND** no secondary binary artifact is produced

#### Scenario: Secondary onefile lands beside primary

- **WHEN** a product passes a secondary binary name plus a secondary import (or entry) on the shared base target
- **THEN** `/dist` includes both the primary onedir artifact and the secondary binary
- **AND** the secondary is built as `--onefile` unless the product opts the secondary into `--onedir` via the documented
  arg
- **AND** the product last stage can `COPY` both from the same Bake export context

#### Scenario: Secondary without identity fails closed

- **WHEN** a secondary is requested without a resolvable secondary import or entry after wheel install
- **THEN** the binary-builder stage fails with a clear error
- **AND** it does not silently skip the secondary

### Requirement: Optional secondary binary contract is documented

Documentation in this repository (at least `docs/ci.md`, and example stubs under `docker/examples/` when present) MUST
describe the secondary build-arg names, the empty/no-op default, onefile-vs-onedir behavior for the secondary, and how a
product last stage copies secondary artifacts from the shared export context. Documentation MUST state that deleting
product-local secondary Dockerfiles (e.g. harvester healthcheck) is a product follow-up after sync, not a Devinfra base
requirement.

#### Scenario: Contributor learns secondary ARG surface

- **WHEN** a contributor reads the product-app Bake / base Dockerfile docs after this change
- **THEN** they learn which build-args enable an optional secondary binary
- **AND** they learn that omitting those args preserves single-primary builds
- **AND** example stubs illustrate copying a secondary from the export context when applicable

### Requirement: Product Dockerfile apk pins use ARG defaults

Product-local Dockerfiles that pin Alpine `apk` packages (typically last-stage / component Dockerfiles under
`docker/Dockerfile.*`, excluding `docker/Dockerfile.product-app.base`) MUST declare each pin as a Dockerfile `ARG`
default whose value is an Alpine package version (`X.Y.Z-rN`), and MUST reference that ARG in `apk add` (e.g.
`"pkg=${PKG_VERSION}"`). They MUST NOT embed Alpine-style inline literals `pkg=X.Y.Z-rN` as the pin source of truth.

The repository MUST provide `scripts/update-dockerfile-pins.sh` that, for each candidate Dockerfile:

1. Detects `ARG <NAME>_VERSION=<apk-ver>` defaults whose value matches Alpine `*-rN` form
2. Maps `<NAME>_VERSION` to apk package `<name>` by stripping `_VERSION`, lower-casing, and replacing `_` with `-`
3. Refreshes those ARG defaults from Alpine APKINDEX (main + community) for the detected Alpine minor
4. Continues to refresh inline pip-style `name==` pins from PyPI when present
5. Exits non-zero (fail loud) when an ARG apk pin’s package is missing from APKINDEX, or when forbidden inline
   `pkg=…-rN` apk literals are present in the file

The script MUST NOT write `*.bak` sidecars. Documentation (`docs/renovate.md` and the script header) MUST state style B
as the fleet convention.

#### Scenario: ARG apk pin is refreshed from APKINDEX

- **WHEN** a product Dockerfile contains `ARG CA_CERTIFICATES_VERSION=20260611-r0` and APKINDEX has a newer
  `ca-certificates` version
- **THEN** running `scripts/update-dockerfile-pins.sh` on that file updates the ARG default to the newer version

#### Scenario: Inline apk version literals fail the updater

- **WHEN** a product Dockerfile contains an Alpine-style inline pin `ca-certificates=20260611-r0`
- **THEN** the updater exits non-zero and reports that inline apk version literals are not supported

#### Scenario: Unknown ARG apk package fails loud

- **WHEN** a Dockerfile declares `ARG SOME_OBSCURE_VERSION=1.0.0-r0` mapping to a package absent from APKINDEX
- **THEN** the updater exits non-zero after reporting the miss (it does not print a successful Done for that file)
