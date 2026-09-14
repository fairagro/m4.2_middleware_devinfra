## MODIFIED Requirements

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

## ADDED Requirements

### Requirement: Lockfile-deterministic binary-builder install is documented

Documentation in this repository (at least `docs/ci.md`) MUST state that `docker/Dockerfile.product-app.base`
`binary-builder` installs transitive dependencies from `uv.lock` and installs built workspace wheels without
re-resolving those dependencies from the live index, so product Bake rebuilds of the same lockfile are
dependency-reproducible (aside from intentionally ARG-pinned tools such as PyInstaller from `versions.env`).

#### Scenario: Contributor reads binary-builder install contract

- **WHEN** a contributor reads the product-app Bake / base Dockerfile docs
- **THEN** they learn binary-builder is lockfile-deterministic for transitive deps
- **AND** they learn wheels are installed without live-index transitive resolution
