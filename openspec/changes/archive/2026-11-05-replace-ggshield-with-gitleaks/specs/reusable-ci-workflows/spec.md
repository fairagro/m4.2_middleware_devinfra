## MODIFIED Requirements

### Requirement: Reusable code-quality workflow

The repository MUST provide `.github/workflows/reusable-code-quality.yml` callable via `workflow_call`. It MUST install
the caller’s Python toolchain from the caller checkout’s `versions.env` via `scripts/load-versions-env.sh` (callers that
sync `versions.env` MUST also sync that script) and run the shared quality bar (format/lint type-check, Bandit with
medium/high fail policy, **vulture**, **import-linter**, **uv audit** lockfile gate, **gitleaks** secret scan, pytest,
and Prettier/markdownlint check scripts) against a configurable package root (Python) plus repository Markdown via npm
scripts. The dependency install step MUST enable uv’s malware check (`UV_MALWARE_CHECK=1` or equivalent). It MUST accept
a boolean `skip` input that still runs the workflow job successfully with a no-op path when true (so required status
checks are not left pending). The default Code Quality job display name MUST remain `Code Quality Check (3.12)` for
branch-ruleset compatibility unless a later change explicitly migrates consumers.

#### Scenario: Product calls code-quality with package root

- **WHEN** a product workflow calls `fairagro/m4.2_middleware_devinfra/.github/workflows/reusable-code-quality.yml` at a
  branch or tag ref with `skip: false` and a package-root input
- **THEN** the reusable job checks out the **caller** repository
- **AND** runs quality checks against that package root using the caller’s `versions.env` Python pin
- **AND** runs Prettier/markdownlint check scripts from the caller’s Node manifest
- **AND** the job reports under the name `Code Quality Check (3.12)`

#### Scenario: Skip no-op for required checks

- **WHEN** the caller passes `skip: true`
- **THEN** the reusable code-quality job completes successfully without running substantive lint/test steps

#### Scenario: Code-quality sync enables malware check

- **WHEN** reusable code-quality installs dependencies with `skip` false
- **THEN** `uv sync` runs with malware check enabled

## ADDED Requirements

### Requirement: Reusable code-quality runs gitleaks

When `skip` is false, `reusable-code-quality.yml` MUST install the caller’s pinned gitleaks (from the caller’s
`versions.env`) and MUST run a gitleaks scan that fails the job on findings. The scan MUST NOT require a GitGuardian or
other SaaS API key. When a repo allowlist file is present (e.g. `.gitleaksignore`), the scan MUST honor it. Missing
gitleaks pin or install failure MUST fail closed.

#### Scenario: CI gitleaks fails on a finding

- **WHEN** reusable code-quality runs with `skip` false and the checkout contains a secret that gitleaks detects and
  that is not allowlisted
- **THEN** the job fails
- **AND** no GitGuardian API key is required

#### Scenario: CI gitleaks respects allowlist

- **WHEN** reusable code-quality runs with `skip` false and the only match is covered by the repo allowlist
- **THEN** the gitleaks step succeeds
