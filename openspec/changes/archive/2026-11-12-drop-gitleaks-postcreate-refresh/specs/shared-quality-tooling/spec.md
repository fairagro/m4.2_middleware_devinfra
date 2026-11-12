## MODIFIED Requirements

### Requirement: Gitleaks CLI pin and install

The repository MUST pin gitleaks via `GITLEAKS_VERSION` in `versions.env` (Renovate-managed) and MUST provide an install
path via the unified pinned-tool installer (e.g. `scripts/install-pinned-tool.sh gitleaks`) that places the pinned
binary on `PATH` for Dev Container **image builds / create paths** and CI. Commit-stage and reusable code-quality MUST
use that installed binary (or an equivalent install-then-run path). The install path MUST fail closed when the pin is
missing. Shared Dev Container **postCreate** MUST NOT refresh gitleaks via that installer; contributors get the pin from
the image after rebuild (same bar as actionlint).

#### Scenario: Contributor has gitleaks after Dev Container rebuild

- **WHEN** a contributor rebuilds the Dev Container with a valid `GITLEAKS_VERSION` pin
- **THEN** `gitleaks` is on `PATH` at that pin without a postCreate `install-pinned-tool.sh gitleaks` refresh
- **AND** the commit-stage gitleaks hook can invoke it without a SaaS API key

#### Scenario: Missing gitleaks pin fails install

- **WHEN** the install path for gitleaks runs without `GITLEAKS_VERSION` set
- **THEN** it exits non-zero with a clear error
