# shared-quality-tooling Specification

## Purpose

Shared commit-stage and pre-push quality tooling (scripts, pre-commit skeleton, bandit, templated
container-structure-test runner) that product repos can sync with minimal local tweaks.

## Requirements

### Requirement: Commit-stage quality helper scripts

The repository MUST provide `scripts/quality-check.sh` and `scripts/quality-fix.sh` that run the shared **commit-stage**
pre-commit hooks only (MUST NOT run the pre-push hook stage). Check MUST be non-mutating validation; fix MUST apply
auto-fixes where hooks support them.

#### Scenario: Contributor runs quality-check

- **WHEN** a contributor runs `scripts/quality-check.sh` with a configured `.pre-commit-config.yaml`
- **THEN** commit-stage hooks run
- **AND** pre-push stage hooks (pytest / container-structure-test) do not run

#### Scenario: Contributor runs quality-fix

- **WHEN** a contributor runs `scripts/quality-fix.sh`
- **THEN** commit-stage hooks run in a mode that applies supported auto-fixes
- **AND** pre-push stage hooks do not run

### Requirement: Shared pre-commit skeleton

The repository MUST provide a root `.pre-commit-config.yaml` that defines:

- **Commit-stage** hooks covering at least: trailing-whitespace / YAML or TOML hygiene, ggshield, ruff, mypy, bandit,
  pylint, and markdownlint (aligned with the product API pattern).
- **Pre-push stage** hooks for `pytest` and container-structure-test that invoke
  `scripts/run-container-structure-test.sh`.

Python-oriented hooks MUST target the `middleware/` package root (per path conventions). Config MUST exclude vendor
agent skill trees that are pinned under `.agents/skills/` (at least `gh`, `docker`, `hadolint`, `uv`, and `scan-secrets`
when present) from hooks that walk the tree (or equivalent exclude lists).

#### Scenario: Pre-commit config lists both stages

- **WHEN** a consumer inspects `.pre-commit-config.yaml`
- **THEN** commit-stage and pre-push stages are both present
- **AND** the pre-push CST entry calls the shared runner script

#### Scenario: Vendor skills are excluded

- **WHEN** commit-stage hooks that scan files run
- **THEN** paths under pinned vendor skill directories (e.g. `.agents/skills/gh/`, `docker/`, `hadolint/`, `uv/`) are
  excluded

### Requirement: Templated container-structure-test runner

The repository MUST provide `scripts/run-container-structure-test.sh` that builds a Docker image and runs
`container-structure-test` against it. Dockerfile path, image tag, and test definition paths MUST be configurable
(arguments and/or environment variables) so product repos can keep local values.

#### Scenario: Runner uses product parameters

- **WHEN** the script is invoked with product-specific Dockerfile, tag, and test paths
- **THEN** it builds that image and runs container-structure-test with those tests
- **AND** it does not hardcode another product’s paths as the only option

### Requirement: Bandit and markdownlint config files

The repository MUST provide a root `.bandit` suitable for `bandit -c`. It MUST provide or retain `.markdownlint.json`,
`.markdownlintignore`, and `.markdownlint-cli2.jsonc` consistent with Prettier and vendor excludes.

#### Scenario: Bandit config exists

- **WHEN** a consumer runs bandit with `-c .bandit` against `middleware/`
- **THEN** the shared `.bandit` file is present at the repo root

### Requirement: Documentation of hook install boundaries

Documentation (README and/or `docs/`) MUST state that commit-stage installation is
`pre-commit install --hook-type pre-commit` (typically Dev Container postCreate / issue #10), and that installing a
pre-push **git** hook that runs the pre-push stage is issue #9 (out of scope for this change’s install steps).

#### Scenario: Contributor reads install docs

- **WHEN** a contributor opens the quality / README docs for this change
- **THEN** they learn how to install the commit-stage hook
- **AND** they learn pre-push git-hook install is deferred to #9
