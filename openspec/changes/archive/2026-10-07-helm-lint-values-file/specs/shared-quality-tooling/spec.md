## MODIFIED Requirements

### Requirement: Commit-stage Helm lint with no-op when no charts

The shared pre-commit skeleton MUST include a **commit-stage** hook that lints product Helm charts. The hook MUST
discover chart roots as directories named `helmchart/<chart>/` or `helm/<chart>/` that contain `Chart.yaml` (one path
segment under `helmchart/` or `helm/`). When **no** such chart exists, the hook MUST succeed without requiring the Helm
CLI. When at least one chart exists, it MUST invoke `helm` from `PATH` (Dev Container pin from `versions.env`
`HELM_VERSION`) and run `helm lint` plus a default-values `helm template` smoke render (same smoke as
`reusable-helm-lint.yml` when `run_template` is true) on each discovered chart. The shared Helm lint runner MUST accept
an optional environment variable `HELM_VALUES_FILE` (path relative to the repository root). When unset or empty, lint
and template MUST use bare-chart behaviour (no `-f`), matching Feature-PR reusable behaviour with empty `values_file`.
When `HELM_VALUES_FILE` is non-empty, the runner MUST fail if that file is missing, and MUST pass `-f` that path to
`helm lint` and to `helm template` for each discovered chart. Missing `helm` while charts exist MUST fail with guidance
to use the Dev Container (or install the pinned Helm version). The hook MUST NOT treat `check-yaml` as Helm validation;
Go-templated chart templates MUST remain excluded from `check-yaml`. Repos without charts (including this Devinfra tree)
MUST remain a successful no-op.

#### Scenario: No chart directories is a no-op

- **WHEN** a contributor runs commit-stage quality (`pre-commit` / `scripts/quality-check.sh`) in a repo with no
  `helmchart/*/Chart.yaml` or `helm/*/Chart.yaml`
- **THEN** the Helm lint hook exits 0
- **AND** it does not fail solely because `helm` is missing from `PATH`

#### Scenario: Existing charts are linted and template-smoked

- **WHEN** a product checkout has at least one `helmchart/<chart>/Chart.yaml` or `helm/<chart>/Chart.yaml`
- **AND** `helm` is on `PATH`
- **AND** `HELM_VALUES_FILE` is unset or empty
- **AND** the contributor runs commit-stage quality
- **THEN** each discovered chart is passed to `helm lint` without `-f`
- **AND** each chart is passed to `helm template` with chart default values (no `-f`)

#### Scenario: HELM_VALUES_FILE overlays lint and template

- **WHEN** at least one chart exists and `helm` is on `PATH`
- **AND** `HELM_VALUES_FILE` points to an existing file relative to the repo root
- **AND** the contributor runs the Helm lint runner
- **THEN** each chart’s `helm lint` and `helm template` invocations include `-f` that path

#### Scenario: Missing HELM_VALUES_FILE fails closed

- **WHEN** at least one chart exists
- **AND** `HELM_VALUES_FILE` is set to a path that does not exist
- **THEN** the runner exits non-zero with a clear error naming the path
- **AND** it does not silently fall back to bare-chart template

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
filter, and that IDE Helm extensions are optional and are **not** the gate. Documentation MUST state that optional
overlay parity uses `HELM_VALUES_FILE` locally and `values_file` on the Feature-PR reusable (same `-f` semantics when
set; bare chart when empty). Helm lint MUST NOT be required as an IDE save/lint extension to satisfy three-environment
parity (named IDE exception, same family as Bandit).

#### Scenario: Contributor reads local vs CI Helm lint

- **WHEN** a contributor opens `docs/quality.md` for Helm / chart quality
- **THEN** they learn local commit-stage lint is the shared hook
- **AND** they learn Feature-PR wiring remains the reusable with a separate detect-changes output
- **AND** they learn `HELM_VALUES_FILE` / `values_file` are the matching overlay knobs
- **AND** they learn IDE Helm tools are not a required third gate
