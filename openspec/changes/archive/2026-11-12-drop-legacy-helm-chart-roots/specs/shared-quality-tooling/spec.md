## MODIFIED Requirements

### Requirement: Shared pre-commit skeleton

The repository MUST provide **two** hand-maintained root pre-commit configs (no required fragment-merge script):

- **Product / Devinfra** — `.pre-commit-config.yaml` covering foundation hygiene (trailing-whitespace / YAML or TOML
  checks with vendor-skill and Helm-template excludes, **gitleaks**, **actionlint**, prettier-md, markdownlint,
  commitlint, commit-path-check), python-product gates (ruff, mypy, bandit, pylint, **vulture**, **import-linter**, **uv
  audit**, pre-push `pytest` + container-structure-test via `scripts/run-container-structure-test.sh`), and gitops
  **helm-lint**
- **Infrastructure** — `.pre-commit-config.infrastructure.yaml` covering the foundation hygiene set above (including
  **actionlint**) plus **helm-lint**, and MUST NOT include `middleware/`-scoped python-product hooks or pre-push
  pytest/CST

Shared foundation/gitops hooks that appear in both files MAY be duplicated; documentation MUST state that policy edits
touch both files when applicable. Consumers MUST NOT need a Devinfra compose script to install hooks.

The pre-push `pytest` hook (product config only) MUST invoke pytest with `-m "not system_external and not system_local"`
(or equivalent), print a short duration / `SKIP=pytest` notice, and MUST NOT be Infra’s required gate. Reusable CI MUST
NOT silently inherit that pre-push marker filter as its only suite.

Python-oriented hooks MUST target the `middleware/` package root. Config MUST exclude vendor agent skill trees under
`.agents/skills/` (at least `gh`, `docker`, `hadolint`, `uv`, and `scan-secrets` when present). Shared `check-yaml` MUST
exclude Go-templated Helm templates under `charts/**/templates/`. The fleet MUST NOT treat `helm/`, `helmchart/`, or
`helmcharts/` as supported chart-root aliases in that exclude list.

Vulture / import-linter / uv-audit / gitleaks / actionlint / quality-CLI pin rules remain in force for hooks present in
the applicable config (confidence 100; product `.importlinter`; `--frozen` uv audit; gitleaks fail-closed without SaaS
key; ruff/mypy/pylint/bandit/vulture/import-linter via `scripts/run-quality-cli.sh` pins; gitleaks and actionlint from
`versions.env`).

Documentation (`docs/quality.md`) MUST describe the two files, the consumer matrix, duplication, and Infra install
(copy/symlink or `PRE_COMMIT_CONFIG_FILE`). Products MUST NOT need post-sync hand-edits of the product root solely for
Helm excludes or the locked hook map.

#### Scenario: Pre-commit config lists both stages

- **WHEN** a python-product consumer inspects `.pre-commit-config.yaml`
- **THEN** commit-stage and pre-push stages are both present
- **AND** the pre-push CST entry calls the shared runner script

#### Scenario: Pre-push pytest excludes system markers

- **WHEN** a contributor inspects the pre-push `pytest` hook entry
- **THEN** pytest is invoked with `-m` excluding `system_external` and `system_local`
- **AND** the entry prints a duration / `SKIP=pytest` notice before pytest runs

#### Scenario: Vendor skills are excluded

- **WHEN** commit-stage hooks that scan files run
- **THEN** paths under pinned vendor skill directories (e.g. `.agents/skills/gh/`, `docker/`, `hadolint/`, `uv/`) are
  excluded

#### Scenario: Helm templates are excluded from check-yaml

- **WHEN** `check-yaml` runs in a product repo that has `charts/*/templates/*.yaml`
- **THEN** those template paths are excluded by the shared config
- **AND** products do not need to patch `.pre-commit-config.yaml` solely for that exclude

#### Scenario: Commit-stage includes vulture

- **WHEN** a python-product consumer inspects commit-stage hooks in `.pre-commit-config.yaml`
- **THEN** a vulture unused-code hook is present for `middleware/`
- **AND** it uses minimum confidence 100 without a synced whitelist file

#### Scenario: Commit-stage includes import-linter

- **WHEN** a python-product consumer inspects commit-stage hooks in `.pre-commit-config.yaml`
- **THEN** an import-linter hook is present that runs the documented runner against product `.importlinter`
- **AND** it fails closed when that config is missing in a product with `middleware/`

#### Scenario: Commit-stage includes uv audit

- **WHEN** a python-product consumer inspects commit-stage hooks in `.pre-commit-config.yaml`
- **THEN** a uv-audit lockfile vulnerability hook is present
- **AND** it fails closed on findings except documented ignored advisory IDs

#### Scenario: Commit-stage includes gitleaks

- **WHEN** a consumer inspects commit-stage hooks in the applicable root config (product or infrastructure)
- **THEN** a gitleaks secret-scan hook is present
- **AND** there is no ggshield secret-scan hook
- **AND** the gitleaks hook does not require `GITGUARDIAN_API_KEY`

#### Scenario: Commit-stage includes actionlint

- **WHEN** a consumer inspects commit-stage hooks in the applicable root config (product or infrastructure)
- **THEN** an actionlint hook is present that runs the `versions.env`-pinned binary on `PATH`
- **AND** the hook is scoped to GitHub workflow files under `.github/workflows/`

#### Scenario: Missing product quality dep does not spawn-fail the gate

- **WHEN** a product checkout runs a synced vulture (or ruff/mypy/pylint/bandit/import-linter) hook or reusable
  code-quality step without that package in its `pyproject.toml`
- **THEN** the gate still invokes the CLI via the synced pin helper instead of failing only because the binary is
  missing from the project env

#### Scenario: pytest stays product-owned

- **WHEN** a contributor inspects pre-push / reusable pytest invocations
- **THEN** they still use the project environment (`uv run pytest` or equivalent)
- **AND** pytest is not required to be listed in the fleet quality-tools requirements file

#### Scenario: Infra config omits python-product hooks

- **WHEN** a contributor inspects `.pre-commit-config.infrastructure.yaml`
- **THEN** the file has no `middleware/`-scoped ruff/mypy/bandit/pylint/vulture/import-linter hooks and no pre-push
  pytest/CST hooks
- **AND** foundation hygiene hooks (including actionlint) and helm-lint remain present

### Requirement: Commit-stage Helm lint with no-op when no charts

Both the product and infrastructure pre-commit roots that include gitops MUST contain a **commit-stage** hook that lints
Helm charts. The hook MUST discover chart roots **only** as directories named `charts/<chart>/` that contain
`Chart.yaml` (one path segment under `charts/`). The fleet MUST NOT discover `helm/`, `helmchart/`, or `helmcharts/` as
chart-root aliases. When **no** such chart exists, the hook MUST succeed without requiring the Helm CLI. When at least
one chart exists, it MUST invoke `helm` from `PATH` (Dev Container pin from `versions.env` `HELM_VERSION`) and run
`helm lint` plus a default-values `helm template` smoke render (same smoke as `reusable-helm-lint.yml` when
`run_template` is true) on each discovered chart. The shared Helm lint runner MUST accept an optional environment
variable `HELM_VALUES_FILE` (path relative to the repository root). When unset or empty, lint and template MUST use
bare-chart behaviour (no `-f`), matching Feature-PR reusable behaviour with empty `values_file`. When `HELM_VALUES_FILE`
is non-empty, the runner MUST fail if that file is missing, and MUST pass `-f` that path to `helm lint` and to
`helm template` for each discovered chart. Missing `helm` while charts exist MUST fail with guidance to use the Dev
Container (or install the pinned Helm). The hook MUST NOT treat `check-yaml` as Helm validation; Go-templated chart
templates MUST remain excluded from `check-yaml`. Repos without charts (including this Devinfra tree) MUST remain a
successful no-op. Documentation MUST state that **`charts/`** is the only fleet chart root.

#### Scenario: No chart directories is a no-op

- **WHEN** a contributor runs commit-stage quality (`pre-commit` / `scripts/quality-check.sh`) in a repo with no
  `charts/*/Chart.yaml`
- **THEN** the Helm lint hook exits 0
- **AND** it does not fail solely because `helm` is missing from `PATH`

#### Scenario: Existing charts are linted and template-smoked

- **WHEN** a product checkout has at least one `charts/<chart>/Chart.yaml`
- **AND** `helm` is on `PATH`
- **AND** `HELM_VALUES_FILE` is unset or empty
- **AND** the contributor runs commit-stage quality
- **THEN** each discovered chart is passed to `helm lint` without `-f`
- **AND** each chart is passed to `helm template` with chart default values (no `-f`)

#### Scenario: Legacy helm and helmchart roots still work during migration

- **WHEN** a product checkout has only `helmchart/<chart>/Chart.yaml` or only `helm/<chart>/Chart.yaml` and no
  `charts/*/Chart.yaml`
- **AND** the contributor runs commit-stage quality
- **THEN** those legacy roots are not discovered
- **AND** the Helm lint hook exits 0 without requiring `helm` on `PATH`

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

- **WHEN** `check-yaml` runs in a product repo that has `charts/*/templates/*.yaml`
- **THEN** those template paths remain excluded
- **AND** Helm validation is the dedicated lint hook, not `check-yaml`

### Requirement: Helm lint local vs Feature-PR documentation

Documentation in this repository (at least `docs/quality.md`) MUST state that commit-stage quality runs Helm lint
locally via the shared hook, that Feature-PR CI still uses `reusable-helm-lint.yml` with a **separate** chart path
filter, and that IDE Helm extensions are optional and are **not** the gate. Documentation MUST state that the canonical
fleet chart root is **`charts/<chart>/`** only, and that `helm/`, `helmchart/`, and `helmcharts/` are not supported
aliases. Documentation MUST state that optional overlay parity uses `HELM_VALUES_FILE` locally and `values_file` on the
Feature-PR reusable (same `-f` semantics when set; bare chart when empty). Helm lint MUST NOT be required as an IDE
save/lint extension to satisfy three-environment parity (named IDE exception, same family as Bandit).

#### Scenario: Contributor reads local vs CI Helm lint

- **WHEN** a contributor opens `docs/quality.md` for Helm / chart quality
- **THEN** they learn local commit-stage lint is the shared hook
- **AND** they learn Feature-PR wiring remains the reusable with a separate detect-changes output
- **AND** they learn `charts/` is the only fleet chart root
- **AND** they learn `HELM_VALUES_FILE` / `values_file` are the matching overlay knobs
- **AND** they learn IDE Helm tools are not a required third gate
