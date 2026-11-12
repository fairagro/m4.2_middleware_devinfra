## MODIFIED Requirements

### Requirement: Feature-PR Helm lint caller documentation

Documentation in this repository (at least `docs/ci.md`) MUST document how products wire `reusable-helm-lint.yml` on
Feature PRs: a **separate** detect-changes output for chart paths (fleet convention `charts/**` only), `skip` wired from
that output, a required `chart_dir` input, and the optional `values_file` input for CI overlays outside chart defaults.
Documentation MUST state that adding chart paths only to the Docker `code` filter is **not** a substitute for this
reusable. Documentation MUST note that commit-stage quality uses the same overlay semantics via `HELM_VALUES_FILE` on
`scripts/run-helm-lint.sh` (see shared quality docs). The recommended Feature-PR snippet MUST use **`charts/`** in
example `chart_dir` / path filters. Documentation MUST NOT present `helm/`, `helmchart/`, or `helmcharts/` as supported
fleet chart roots. Chart-only PRs MUST be able to skip Docker build/check while still running Helm lint when chart paths
change.

#### Scenario: Maintainer wires Helm lint without forcing Docker build

- **WHEN** a product maintainer reads the Feature-PR CI docs after this change
- **THEN** they find `reusable-helm-lint.yml` with a separate chart path filter and `skip` wiring
- **AND** example paths use `charts/` as the fleet convention
- **AND** they learn not to rely on stuffing chart paths into the Docker `code` filter alone
- **AND** they learn optional `values_file` can pass a product CI overlay into lint/template smoke
- **AND** they learn local commit-stage overlay uses `HELM_VALUES_FILE` for the same `-f` semantics
