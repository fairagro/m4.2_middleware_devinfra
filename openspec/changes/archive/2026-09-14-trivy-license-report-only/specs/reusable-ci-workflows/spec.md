## MODIFIED Requirements

### Requirement: Reusable check workflow

The repository MUST provide `.github/workflows/reusable-check.yml` callable via `workflow_call`. When `skip` is false it
MUST run licence scanning, vulnerability scanning (with SARIF upload where configured), and container-structure tests
against Docker image (and SBOM) artifacts produced by a prior build job in the same workflow run. Licence scanning MUST
remain a dedicated job (display name **Licence Check**) and MUST NOT fail the job on Trivy license findings (report /
artifact only). Vulnerability scanning fail policy MUST remain unchanged by this requirement. Artifact names and local
image tag construction MUST be parameterized (at least component list, version string, and image base name) so products
are not hard-locked to a single product’s naming. The workflow MUST document (in-repo docs and/or workflow comments) the
expected artifact contract so callers can satisfy it with a local or future shared build workflow. When `skip` is true,
required check jobs MUST still complete successfully via a no-op path where branch protection requires a status.

#### Scenario: Check consumes build artifacts

- **WHEN** a product workflow has uploaded artifacts matching the documented contract and calls the reusable check
  workflow with `skip: false`, version, components, and image base name
- **THEN** licence, security, and container-structure jobs consume those artifacts
- **AND** scans/tests target the loaded image (and SBOM where applicable) for each component

#### Scenario: Check skip no-op

- **WHEN** the caller passes `skip: true`
- **THEN** the reusable check path completes successfully without requiring build artifacts

#### Scenario: Licence findings do not fail check

- **WHEN** Trivy license scanning reports HIGH/CRITICAL or `restricted` classifications (e.g. Alpine GPL packages)
- **AND** `skip` is false
- **THEN** the Licence Check job still completes successfully
- **AND** vulnerability / SBOM scan jobs are not relaxed by this behaviour

## ADDED Requirements

### Requirement: Release body includes Trivy license summary

When `reusable-release.yml` creates a GitHub Release (`create_github_release: true`, not skipped), the release body MUST
include a readable **license** section derived from a Trivy license scan of each released component image (re-scan in
the release workflow; MUST NOT require check-job artifacts). The section MUST include short summary counts by
classification and/or severity and a package → license → classification listing (MAY truncate with a pointer to the job
log when large). License findings MUST NOT fail the release solely because licenses were found.

#### Scenario: GitHub Release lists image licenses

- **WHEN** a product workflow creates a GitHub Release via the reusable Docker release workflow with `skip: false`
- **THEN** the release body contains a license section for the released component image(s)
- **AND** the release is not failed solely due to Trivy license classifications on Alpine base packages
