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
