# reusable-ci-workflows Specification

## Purpose

Canonical reusable GitHub Actions workflows for shared code-quality and image/SBOM check stages so m4.2 product repos
call Devinfra by `uses:` instead of copying YAML.

## Requirements

### Requirement: Reusable code-quality workflow

The repository MUST provide `.github/workflows/reusable-code-quality.yml` callable via `workflow_call`. It MUST install
the caller’s Python toolchain from the caller checkout’s `versions.env` (via the shared load-versions pattern when
present) and run the shared quality bar (format/lint type-check, Bandit with medium/high fail policy, and pytest)
against a configurable package root. It MUST accept a boolean `skip` input that still runs the workflow job successfully
with a no-op path when true (so required status checks are not left pending). The default Code Quality job display name
MUST remain `Code Quality Check (3.12)` for branch-ruleset compatibility unless a later change explicitly migrates
consumers.

#### Scenario: Product calls code-quality with package root

- **WHEN** a product workflow calls `fairagro/m4.2_middleware_devinfra/.github/workflows/reusable-code-quality.yml` at a
  branch or tag ref with `skip: false` and a package-root input
- **THEN** the reusable job checks out the **caller** repository
- **AND** runs quality checks against that package root using the caller’s `versions.env` Python pin
- **AND** the job reports under the name `Code Quality Check (3.12)`

#### Scenario: Skip no-op for required checks

- **WHEN** the caller passes `skip: true`
- **THEN** the reusable code-quality job completes successfully without running substantive lint/test steps

### Requirement: Reusable check workflow

The repository MUST provide `.github/workflows/reusable-check.yml` callable via `workflow_call`. When `skip` is false it
MUST run licence scanning, vulnerability scanning (with SARIF upload where configured), and container-structure tests
against Docker image (and SBOM) artifacts produced by a prior build job in the same workflow run. Artifact names and
local image tag construction MUST be parameterized (at least component list, version string, and image base name) so
products are not hard-locked to a single product’s naming. The workflow MUST document (in-repo docs and/or workflow
comments) the expected artifact contract so callers can satisfy it with a local or future shared build workflow. When
`skip` is true, required check jobs MUST still complete successfully via a no-op path where branch protection requires a
status.

#### Scenario: Check consumes build artifacts

- **WHEN** a product workflow has uploaded artifacts matching the documented contract and calls the reusable check
  workflow with `skip: false`, version, components, and image base name
- **THEN** licence, security, and container-structure jobs consume those artifacts
- **AND** scans/tests target the loaded image (and SBOM where applicable) for each component

#### Scenario: Check skip no-op

- **WHEN** the caller passes `skip: true`
- **THEN** the reusable check path completes successfully without requiring build artifacts

### Requirement: Consumer call documentation

Documentation in this repository MUST explain how a product PR (or release) workflow calls both reusable workflows with
`uses: fairagro/m4.2_middleware_devinfra/.github/workflows/<file>@<ref>`, which inputs to pass, the artifact contract
for check, and that `@main` is acceptable for early adoption while pinning to a tag or commit SHA is recommended for
stability. Documentation MUST state that shared **build/release** reusables are out of this capability’s MVP.

#### Scenario: Contributor reads CI docs

- **WHEN** a contributor opens the CI documentation for adopting shared workflows
- **THEN** they learn the `uses:` pattern with branch or tag refs
- **AND** they learn required inputs and the check artifact contract
- **AND** they learn build/release reusables are deferred
