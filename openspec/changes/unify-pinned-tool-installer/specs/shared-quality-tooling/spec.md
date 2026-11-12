## ADDED Requirements

### Requirement: Unified pinned-tool installer

The repository MUST provide a single install driver (e.g. `scripts/install-pinned-tool.sh <tool>`) for at least
`gitleaks`, `actionlint`, `kubeconform`, `cst`, and `git-cliff`, loading `versions.env` directly (not
`load-versions-env.sh`), failing closed on missing pin/file/unknown id, and supporting `sudo`. Per-tool
`scripts/install-*.sh` shims for those tools MUST NOT remain.

#### Scenario: Contributor installs a named tool via the driver

- **WHEN** a contributor or CI runs `bash scripts/install-pinned-tool.sh gitleaks` with a valid `GITLEAKS_VERSION` pin
- **THEN** `gitleaks` is on `PATH` at that pin

#### Scenario: Unknown tool id fails closed

- **WHEN** the driver is invoked with an unsupported tool id
- **THEN** it exits non-zero with a clear error

#### Scenario: Missing pin fails closed under sudo-safe load

- **WHEN** the driver runs for a supported tool and that tool’s `*_VERSION` pin is unset
- **THEN** it exits non-zero without having sourced `load-versions-env.sh`

#### Scenario: Dockerfile may keep inline downloads

- **WHEN** a contributor reads quality or Dev Container docs for pinned CLI install
- **THEN** they learn the product image MAY keep inline `RUN` downloads for the same pins
- **AND** image-via-driver is documented as a separate follow-up

## MODIFIED Requirements

### Requirement: Gitleaks CLI pin and install

The repository MUST pin gitleaks via `GITLEAKS_VERSION` in `versions.env` (Renovate-managed) and MUST provide an install
path via the unified pinned-tool installer (e.g. `scripts/install-pinned-tool.sh gitleaks`) that places the pinned
binary on `PATH` for Dev Container post-create and CI. Commit-stage and reusable code-quality MUST use that installed
binary (or an equivalent install-then-run path). The install path MUST fail closed when the pin is missing.

#### Scenario: Contributor has gitleaks after Dev Container create

- **WHEN** Dev Container post-create runs with a valid `GITLEAKS_VERSION` pin
- **THEN** `gitleaks` is on `PATH` at that pin
- **AND** the commit-stage gitleaks hook can invoke it without a SaaS API key

#### Scenario: Missing gitleaks pin fails install

- **WHEN** the install path for gitleaks runs without `GITLEAKS_VERSION` set
- **THEN** it exits non-zero with a clear error

### Requirement: Actionlint CLI pin and install

The repository MUST pin actionlint via `ACTIONLINT_VERSION` in `versions.env` (Renovate-managed) and MUST provide an
install path via the unified pinned-tool installer (e.g. `scripts/install-pinned-tool.sh actionlint`) that places the
pinned binary on `PATH` for Dev Container image builds / create paths and CI. Commit-stage hooks and reusable
code-quality MUST use that installed binary (or an equivalent install-then-run path from the same pin). The install path
MUST fail closed when the pin is missing. Docs MUST state that the same `ACTIONLINT_VERSION` applies to local hooks and
GitHub Actions (no second pin via pre-commit `rev`).

#### Scenario: Contributor has actionlint after Dev Container rebuild

- **WHEN** a contributor rebuilds the Dev Container with a valid `ACTIONLINT_VERSION` pin
- **THEN** `actionlint` is on `PATH` at that pin
- **AND** the commit-stage actionlint hook can invoke it

#### Scenario: Missing actionlint pin fails install

- **WHEN** the install path for actionlint runs without `ACTIONLINT_VERSION` set
- **THEN** it exits non-zero with a clear error

### Requirement: Kubeconform CLI pin and install

The repository MUST pin kubeconform via `KUBECONFORM_VERSION` in `versions.env` (Renovate-managed) and MUST provide an
install path via the unified pinned-tool installer (e.g. `scripts/install-pinned-tool.sh kubeconform`) that places the
pinned binary on `PATH` for Dev Container image builds / create paths and consumer CI. The install path MUST fail closed
when the pin is missing. Docs MUST state that the same pin applies locally and in CI (no second pin source).

#### Scenario: Contributor has kubeconform after Dev Container rebuild

- **WHEN** a contributor rebuilds the Dev Container with a valid `KUBECONFORM_VERSION` pin
- **THEN** `kubeconform` is on `PATH` at that pin

#### Scenario: Missing kubeconform pin fails install

- **WHEN** the install path for kubeconform runs without `KUBECONFORM_VERSION` set
- **THEN** it exits non-zero with a clear error
