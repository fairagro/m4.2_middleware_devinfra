## MODIFIED Requirements

### Requirement: Reusable code-quality workflow

The repository MUST provide `.github/workflows/reusable-code-quality.yml` callable via `workflow_call`. It MUST install
the caller’s Python toolchain from the caller checkout’s `versions.env` via `scripts/load-versions-env.sh` (callers that
sync `versions.env` MUST also sync that script) and run the shared quality bar (format/lint type-check, Bandit with
medium/high fail policy, **vulture**, **uv audit** lockfile gate, pytest, and Prettier/markdownlint check scripts)
against a configurable package root (Python) plus repository Markdown via npm scripts. The dependency install step MUST
enable uv’s malware check (`UV_MALWARE_CHECK=1` or equivalent). It MUST accept a boolean `skip` input that still runs
the workflow job successfully with a no-op path when true (so required status checks are not left pending). The default
Code Quality job display name MUST remain `Code Quality Check (3.12)` for branch-ruleset compatibility unless a later
change explicitly migrates consumers.

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

### Requirement: Reusable code-quality runs uv audit

When `skip` is false, `reusable-code-quality.yml` MUST run `uv audit` against the caller lockfile with the same fail
policy as the commit-stage uv-audit hook (frozen lockfile; fail on non-ignored findings). A non-ignored advisory MUST
fail the job.

#### Scenario: CI uv audit matches hook policy

- **WHEN** reusable code-quality runs with `skip` false
- **THEN** it executes uv audit with the shared frozen/ignore policy
- **AND** a non-ignored finding fails the workflow
