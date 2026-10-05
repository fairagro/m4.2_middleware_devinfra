## ADDED Requirements

### Requirement: Reusable Helm lint workflow

The repository MUST provide `.github/workflows/reusable-helm-lint.yml` callable via `workflow_call`. When `skip` is
false it MUST check out the caller repository, install Helm from the caller checkout’s `versions.env` (`HELM_VERSION`)
via the shared versions-load pattern used by other Helm reusables, and run `helm lint` against a required `chart_dir`
input (path relative to the caller checkout). It MUST accept a boolean `skip` input that completes the job successfully
with a no-op path when true (so required status checks are not left pending). It MUST accept a boolean input that
enables an optional `helm template` smoke render of the same chart (default **true**); when that input is false, only
`helm lint` is required. The workflow MUST NOT publish OCI packages or create GitHub Releases. It MUST NOT require chart
paths to be included in the Docker Feature-PR `code` detect-changes filter.

#### Scenario: Helm lint runs for chart changes

- **WHEN** a product Feature-PR caller invokes `reusable-helm-lint.yml` with `skip: false` and a valid `chart_dir`
- **THEN** the job installs the pinned Helm version and runs `helm lint` on that directory
- **AND** when the template smoke input is true it also runs `helm template` successfully against the chart

#### Scenario: Skip completes without lint

- **WHEN** a caller sets `skip: true`
- **THEN** the Helm lint job completes successfully without failing on a missing or unchanged chart
- **AND** it does not leave a required check pending

#### Scenario: Template smoke can be disabled

- **WHEN** a caller sets the template smoke input to false and `skip` is false
- **THEN** the job still runs `helm lint`
- **AND** it does not require `helm template` to succeed

### Requirement: Feature-PR Helm lint caller documentation

Documentation in this repository (at least `docs/ci.md`) MUST document how products wire `reusable-helm-lint.yml` on
Feature PRs: a **separate** detect-changes output for chart paths (product-local roots such as `helmchart/**` or
`helm/**`), `skip` wired from that output, and a required `chart_dir` input. Documentation MUST state that adding chart
paths only to the Docker `code` filter is **not** a substitute for this reusable. The recommended Feature-PR snippet MAY
show the Helm lint job alongside quality/build/check; chart-only PRs MUST be able to skip Docker build/check while still
running Helm lint when chart paths change.

#### Scenario: Maintainer wires Helm lint without forcing Docker build

- **WHEN** a product maintainer reads the Feature-PR CI docs after this change
- **THEN** they find `reusable-helm-lint.yml` with a separate chart path filter and `skip` wiring
- **AND** they learn not to rely on stuffing chart paths into the Docker `code` filter alone

## MODIFIED Requirements

### Requirement: Feature-PR and release concurrency caller documentation

Documentation in this repository (at least `docs/ci.md`) MUST provide a **complete recommended Feature-PR caller**
snippet that includes: (1) workflow-level `concurrency` grouped by PR number (or equivalent) with
`cancel-in-progress: true`; (2) a full `detect-changes` job using a paths-filter action with a **suggested default**
path set for a `code` (or equivalent) output, plus a note that products may extend the filter (e.g. `stubs/`,
`docker-bake.hcl`, `versions.env`); (3) wiring `skip` from that output into reusable code-quality / build / check, and
the check job `if:` / build-result combination consistent with the existing skip contract; (4) when the product has a
Helm chart, a **separate** chart-path detect-changes output and `skip` wiring into `reusable-helm-lint.yml` (chart paths
MUST NOT be documented as belonging only in the Docker `code` filter). Documentation MUST also guide **release /
pre-release / Helm** callers to prefer a concurrency group that serializes overlapping runs of the same workflow+ref
with `cancel-in-progress: false`, and MUST state that `detect-changes` / `skip` is Feature-PR-oriented and not required
for dispatch release callers. Documentation MUST state explicitly that reusable-level concurrency does not replace
caller-level cancel for the full PR pipeline, and that `skip` remains a **caller** responsibility (`detect-changes`
stays product-local).

#### Scenario: Contributor copies Feature-PR concurrency and detect-changes

- **WHEN** a product maintainer reads the Feature-PR section of the CI docs after this change
- **THEN** they see workflow-level cancel-in-progress concurrency
- **AND** they see a full `detect-changes` job with a suggested path filter and `skip` wiring into quality/build/check
- **AND** they see separate chart-path filter guidance for `reusable-helm-lint` when the product ships a chart
- **AND** they learn reusable concurrency does not replace that caller-level cancel

#### Scenario: Contributor configures release concurrency

- **WHEN** a product maintainer reads the release / Helm caller guidance after this change
- **THEN** they learn to serialize with `cancel-in-progress: false`
- **AND** they learn `detect-changes` is not required for those dispatch callers
