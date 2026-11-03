## ADDED Requirements

### Requirement: Trivy Action binary follows versions.env TRIVY_VERSION

When `reusable-check.yml` or `reusable-release.yml` invokes `aquasecurity/trivy-action` with `skip` false (or the
equivalent non-skipped release path), the workflow MUST obtain `TRIVY_VERSION` from the **caller** repository checkout’s
repo-root `versions.env` (same fail-closed read pattern used for `UV_VERSION` elsewhere in fleet workflows) and MUST
pass that value as the Action’s `version` input on **every** such invocation in those two workflows (image, SBOM, and
license scans as applicable). The workflow MUST fail closed with a clear error when `TRIVY_VERSION` is missing or empty.
Documentation (`docs/ci.md`) MUST state that the CI Trivy **binary** follows `versions.env` / Renovate and is
independent of the pinned Trivy Action SHA. This MUST NOT change Licence Check report-only exit behaviour or Security
Check CRITICAL/HIGH fail policy.

#### Scenario: Check Trivy steps use versions.env pin

- **WHEN** a product calls `reusable-check.yml` with `skip: false` and the caller checkout has a non-empty
  `TRIVY_VERSION` in `versions.env`
- **THEN** every `trivy-action` step in Licence Check and Security Check runs with that version as the Action `version`
  input

#### Scenario: Missing TRIVY_VERSION fails closed

- **WHEN** `skip` is false (or the release Trivy license path runs) and `TRIVY_VERSION` is missing or empty in the
  caller `versions.env`
- **THEN** the job fails before or at Trivy invocation with an error naming `TRIVY_VERSION` / `versions.env`

#### Scenario: Release Trivy license scan uses the same pin

- **WHEN** `reusable-release.yml` runs its Trivy license scan for the release body
- **THEN** that `trivy-action` step also receives `version` from the caller `versions.env` `TRIVY_VERSION`
