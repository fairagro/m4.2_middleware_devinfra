## MODIFIED Requirements

### Requirement: Reusable Helm lint workflow

The repository MUST provide `.github/workflows/reusable-helm-lint.yml` callable via `workflow_call`. When `skip` is
false it MUST check out the caller repository, install Helm from the caller checkout’s `versions.env` (`HELM_VERSION`)
via the shared versions-load pattern used by other Helm reusables, and run `helm lint` against a required `chart_dir`
input (path relative to the caller checkout). It MUST accept a boolean `skip` input that completes the job successfully
with a no-op path when true (so required status checks are not left pending). It MUST accept a boolean input that
enables an optional `helm template` smoke render of the same chart (default **true**); when that input is false, only
`helm lint` is required. It MUST accept an optional string input `values_file` (default empty) that is a path relative
to the caller checkout. When `values_file` is non-empty and `skip` is false, the workflow MUST fail if that file is
missing, and MUST pass `-f` that path to `helm lint` and (when template smoke is enabled) to `helm template`. When
`values_file` is empty, lint and template MUST keep bare-chart behaviour (no `-f`). The workflow MUST NOT publish OCI
packages or create GitHub Releases. It MUST NOT require chart paths to be included in the Docker Feature-PR `code`
detect-changes filter.

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

#### Scenario: Optional values_file overlays lint and template

- **WHEN** a caller sets a non-empty `values_file` to an existing path and `skip` is false
- **THEN** `helm lint` is invoked with `-f` that path
- **AND** when template smoke is enabled, `helm template` is also invoked with `-f` that path

#### Scenario: Missing values_file fails closed

- **WHEN** a caller sets a non-empty `values_file` that does not exist in the checkout and `skip` is false
- **THEN** the job fails with a clear error naming the missing path
- **AND** it does not silently fall back to bare-chart template

### Requirement: Feature-PR Helm lint caller documentation

Documentation in this repository (at least `docs/ci.md`) MUST document how products wire `reusable-helm-lint.yml` on
Feature PRs: a **separate** detect-changes output for chart paths (product-local roots such as `helmchart/**` or
`helm/**`), `skip` wired from that output, a required `chart_dir` input, and the optional `values_file` input for CI
overlays outside chart defaults. Documentation MUST state that adding chart paths only to the Docker `code` filter is
**not** a substitute for this reusable. Documentation MUST note that commit-stage quality uses the same overlay
semantics via `HELM_VALUES_FILE` on `scripts/run-helm-lint.sh` (see shared quality docs). The recommended Feature-PR
snippet MAY show the Helm lint job alongside quality/build/check and MAY show an example `values_file` path; chart-only
PRs MUST be able to skip Docker build/check while still running Helm lint when chart paths change.

#### Scenario: Maintainer wires Helm lint without forcing Docker build

- **WHEN** a product maintainer reads the Feature-PR CI docs after this change
- **THEN** they find `reusable-helm-lint.yml` with a separate chart path filter and `skip` wiring
- **AND** they learn not to rely on stuffing chart paths into the Docker `code` filter alone
- **AND** they learn optional `values_file` can pass a product CI overlay into lint/template smoke
- **AND** they learn local commit-stage overlay uses `HELM_VALUES_FILE` for the same `-f` semantics
