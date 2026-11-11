## ADDED Requirements

### Requirement: Kubeconform CLI pin and install

The repository MUST pin kubeconform via `KUBECONFORM_VERSION` in `versions.env` (Renovate-managed) and MUST provide an
install helper (e.g. `scripts/install-kubeconform.sh`) that places the pinned binary on `PATH` for Dev Container image
builds / create paths and consumer CI. The install helper MUST fail closed when the pin is missing. Docs MUST state that
the same pin applies locally and in CI (no second pin source).

#### Scenario: Contributor has kubeconform after Dev Container rebuild

- **WHEN** a contributor rebuilds the Dev Container with a valid `KUBECONFORM_VERSION` pin
- **THEN** `kubeconform` is on `PATH` at that pin

#### Scenario: Missing kubeconform pin fails install

- **WHEN** the install helper runs without `KUBECONFORM_VERSION` set
- **THEN** it exits non-zero with a clear error

### Requirement: Generic kubeconform runner

The repository MUST provide a thin shared runner (e.g. `scripts/run-kubeconform.sh`) that invokes `kubeconform` on
`PATH` for caller-supplied file arguments and/or stdin, forwards extra CLI flags unchanged, and fails closed when the
binary is missing. The runner MUST NOT discover charts, run `helm template`, or ship fleet-default CRD schema packs.

#### Scenario: Runner validates supplied manifests

- **WHEN** a consumer CI script pipes rendered YAML or passes manifest file paths to the shared kubeconform runner
- **THEN** kubeconform runs against that input with any forwarded flags
- **AND** the runner does not call `helm template` or scan `charts/` on its own

#### Scenario: Missing kubeconform binary fails the runner

- **WHEN** the runner is invoked and `kubeconform` is not on `PATH`
- **THEN** it exits non-zero with a clear error

#### Scenario: CRD policy stays consumer-owned

- **WHEN** a contributor reads quality docs for kubeconform
- **THEN** they learn CRD schemas and flags such as `-ignore-missing-schemas` are consumer policy
- **AND** the shared runner does not embed a fleet-default CRD pack

### Requirement: Kubeconform stays opt-in for product helm-lint

Product `run-helm-lint.sh` and shared pre-commit helm-lint hooks MUST NOT require kubeconform by default. Documentation
(`docs/quality.md`) MUST contrast kubeconform with helm lint/template smoke and MUST point consumers (e.g. Infra matrix
wiring) at the shared pin, install helper, and runner without mandating product hook hard-fail.

#### Scenario: Product helm-lint does not invoke kubeconform

- **WHEN** a contributor inspects `scripts/run-helm-lint.sh` and the shared helm-lint pre-commit entries
- **THEN** those paths do not invoke kubeconform as a required step
- **AND** quality docs describe kubeconform as an opt-in consumer gate after render
