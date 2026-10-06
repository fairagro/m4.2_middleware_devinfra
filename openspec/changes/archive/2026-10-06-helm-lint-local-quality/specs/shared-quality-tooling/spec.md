## ADDED Requirements

### Requirement: Commit-stage Helm lint with no-op when no charts

The shared pre-commit skeleton MUST include a **commit-stage** hook that lints product Helm charts. The hook MUST
discover chart roots as directories named `helmchart/<chart>/` or `helm/<chart>/` that contain `Chart.yaml` (one path
segment under `helmchart/` or `helm/`). When **no** such chart exists, the hook MUST succeed without requiring the Helm
CLI. When at least one chart exists, it MUST invoke `helm` from `PATH` (Dev Container pin from `versions.env`
`HELM_VERSION`) and run `helm lint` plus a default-values `helm template` smoke render (same smoke as
`reusable-helm-lint.yml` when `run_template` is true) on each discovered chart. Missing `helm` while charts exist MUST
fail with guidance to use the Dev Container (or install the pinned Helm version). The hook MUST NOT treat `check-yaml`
as Helm validation; Go-templated chart templates MUST remain excluded from `check-yaml`. Repos without charts (including
this Devinfra tree) MUST remain a successful no-op.

#### Scenario: No chart directories is a no-op

- **WHEN** a contributor runs commit-stage quality (`pre-commit` / `scripts/quality-check.sh`) in a repo with no
  `helmchart/*/Chart.yaml` or `helm/*/Chart.yaml`
- **THEN** the Helm lint hook exits 0
- **AND** it does not fail solely because `helm` is missing from `PATH`

#### Scenario: Existing charts are linted and template-smoked

- **WHEN** a product checkout has at least one `helmchart/<chart>/Chart.yaml` or `helm/<chart>/Chart.yaml`
- **AND** `helm` is on `PATH`
- **AND** the contributor runs commit-stage quality
- **THEN** each discovered chart is passed to `helm lint`
- **AND** each chart is passed to `helm template` with chart default values

#### Scenario: Charts present without helm fails closed

- **WHEN** at least one discovered chart exists
- **AND** `helm` is not on `PATH`
- **THEN** the hook exits non-zero
- **AND** the message points at the Dev Container / `HELM_VERSION` pin

#### Scenario: check-yaml still excludes Helm templates

- **WHEN** `check-yaml` runs in a product repo that has `helm/` or `helmchart/*/templates/*.yaml`
- **THEN** those template paths remain excluded
- **AND** Helm validation is the dedicated lint hook, not `check-yaml`

### Requirement: Helm lint local vs Feature-PR documentation

Documentation in this repository (at least `docs/quality.md`) MUST state that commit-stage quality runs Helm lint
locally via the shared hook, that Feature-PR CI still uses `reusable-helm-lint.yml` with a **separate** chart path
filter, and that IDE Helm extensions are optional and are **not** the gate. Helm lint MUST NOT be required as an IDE
save/lint extension to satisfy three-environment parity (named IDE exception, same family as Bandit).

#### Scenario: Contributor reads local vs CI Helm lint

- **WHEN** a contributor opens `docs/quality.md` for Helm / chart quality
- **THEN** they learn local commit-stage lint is the shared hook
- **AND** they learn Feature-PR wiring remains the reusable with a separate detect-changes output
- **AND** they learn IDE Helm tools are not a required third gate
