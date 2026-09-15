# shared-codeql Specification

## Purpose

Defines the thin synced CodeQL analysis workflow so Devinfra and product consumers share one CodeQL SoT with fleet
toolchain pins from `versions.env`, without product Renovate shadow bumps on hardcoded workflow pins.

## Requirements

### Requirement: Shared CodeQL workflow is present

The repository MUST provide `.github/workflows/codeql.yml` as the canonical thin CodeQL analysis workflow for Devinfra
and for product sync. The workflow MUST NOT be named `reusable-*.yml`. It MUST analyze at least languages `actions` and
`python` with `build-mode: none` and `fail-fast: false` across the matrix.

#### Scenario: Fresh clone has CodeQL workflow

- **WHEN** a contributor clones the repository
- **THEN** `.github/workflows/codeql.yml` is present
- **AND** the workflow is not under the `reusable-*.yml` naming pattern

### Requirement: CodeQL triggers are PR-main plus weekly

The CodeQL workflow MUST run on `pull_request` (at least types opened, synchronize, reopened) targeting `main`, and on a
weekly `schedule` cron. It MUST NOT use `push` triggers on feature, issue, or main branches as the primary analysis
path.

#### Scenario: Maintainer inspects CodeQL triggers

- **WHEN** a maintainer opens `.github/workflows/codeql.yml`
- **THEN** they find `pull_request` to `main` and a weekly schedule
- **AND** they do not find `push` branch filters such as `feature/*` as the sole or primary trigger

### Requirement: CodeQL toolchain pins come from versions.env

For the Python matrix job, the workflow MUST obtain `PYTHON_VERSION` and `UV_VERSION` from repo-root `versions.env` (via
`scripts/load-versions-env.sh` or equivalent) and MUST NOT hardcode those version strings in the workflow YAML. Action
references MUST follow the same pinning style as other shared workflows (major or patch tags as used elsewhere — not
product-local literal toolchain strings). Python dependency install MUST use `uv python install` for the pinned
interpreter and `uv sync --dev --all-packages` (or an equivalent workspace-wide frozen sync).

#### Scenario: Python job uses fleet pins

- **WHEN** the CodeQL Python matrix job runs in a repo that has `versions.env` and `scripts/load-versions-env.sh`
- **THEN** uv/Python versions come from that SoT
- **AND** the job does not embed divergent hardcoded `3.12.x` / `0.12.x` toolchain strings
- **AND** dependencies are installed with a workspace-wide `uv sync --dev --all-packages` (or equivalent)

### Requirement: CodeQL workflow is documented

Documentation (`docs/ci.md` and/or `docs/renovate.md`) MUST state that `.github/workflows/codeql.yml` is Devinfra SoT,
synced to products, uses `versions.env` for toolchain pins, and that product Renovate must not bump that file.

#### Scenario: Contributor reads CodeQL docs

- **WHEN** a contributor opens CI or Renovate docs
- **THEN** they learn CodeQL is shared via sync
- **AND** they learn toolchain pins stay in `versions.env`
