## MODIFIED Requirements

### Requirement: Shared pre-commit skeleton

The repository MUST provide a root `.pre-commit-config.yaml` that defines:

- **Commit-stage** hooks covering at least: trailing-whitespace / YAML or TOML hygiene, **gitleaks** (secret scan),
  ruff, mypy, bandit, pylint, **vulture**, **import-linter**, **uv audit** (Python lockfile CVE gate), and markdownlint
  (aligned with the product API pattern).
- **Pre-push stage** hooks for `pytest` and container-structure-test that invoke
  `scripts/run-container-structure-test.sh`.

The pre-push `pytest` hook MUST invoke pytest with marker expression `-m "not system_external and not system_local"` (or
an equivalent expression that excludes those two markers) so heavy system suites are not the default local push gate.
Before running pytest, the hook entry MUST print a short notice that the stage may take several minutes and that
`SKIP=pytest` can skip the hook (escape hatch only). Reusable CI / product CI MUST NOT silently inherit that pre-push
marker filter as their only suite; broader CI runs stay explicit.

Python-oriented hooks MUST target the `middleware/` package root (per path conventions). Config MUST exclude vendor
agent skill trees that are pinned under `.agents/skills/` (at least `gh`, `docker`, `hadolint`, `uv`, and `scan-secrets`
when present) from hooks that walk the tree (or equivalent exclude lists). The shared `check-yaml` hook MUST also
exclude Go-templated Helm chart templates under `charts/**/templates/`, and during the migration window also under
`helm/**/templates/` and `helmchart/**/templates/` (harmless when those paths are absent), so product repos can adopt
`.pre-commit-config.yaml` verbatim without post-sync hand-edits for Helm. The fleet MUST NOT treat `helmcharts/` as a
supported chart-root alias in that exclude list.

The commit-stage **vulture** hook MUST match the reusable code-quality vulture fail policy (minimum confidence 100; no
synced whitelist file). The commit-stage **import-linter** hook MUST run against the product-owned **`.importlinter`**
(fleet-required settings documented in `docs/quality.md`). The commit-stage **uv audit** hook MUST match the reusable
code-quality uv-audit fail policy (audit the project lockfile with `--frozen` or equivalent; fail on any reported
vulnerability / adverse status except IDs listed via the documented ignore mechanism).

The commit-stage **gitleaks** hook MUST fail closed on findings for the staged change set (pre-commit / protect mode or
equivalent). It MUST NOT require a GitGuardian or other SaaS API key. Allowlisted false positives MUST be expressible
via a repo-owned allowlist file (e.g. `.gitleaksignore`) documented in quality docs.

Commit-stage and reusable code-quality invocations of **ruff**, **mypy**, **pylint**, **bandit**, **vulture**, and
**import-linter** MUST obtain those CLIs via a synced fleet pin file (e.g. `scripts/quality-tools-pins.txt` via
`scripts/run-quality-cli.sh`) so a product that has not listed the tool in `pyproject.toml` still runs the gate instead
of failing with a missing-binary / `Failed to spawn` error. **gitleaks** MUST NOT be listed in that Python pin file; it
MUST be installed from the `versions.env` pin (same pattern as other release CLIs). **pytest** and application/runtime
dependencies MAY remain product-owned project deps. Documentation MUST state that products MAY optionally keep the
Python quality CLIs in the project env for IDE extensions. Documentation MUST NOT require `GITGUARDIAN_API_KEY` for the
fleet secret-scan gate.

#### Scenario: Pre-commit config lists both stages

- **WHEN** a consumer inspects `.pre-commit-config.yaml`
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

- **WHEN** `check-yaml` runs in a product repo that has `charts/`, `helm/`, or `helmchart/*/templates/*.yaml`
- **THEN** those template paths are excluded by the shared config
- **AND** products do not need to patch synced `.pre-commit-config.yaml` solely for that exclude

#### Scenario: Commit-stage includes vulture

- **WHEN** a consumer inspects commit-stage hooks in `.pre-commit-config.yaml`
- **THEN** a vulture unused-code hook is present for `middleware/`
- **AND** it uses minimum confidence 100 without a synced whitelist file

#### Scenario: Commit-stage includes import-linter

- **WHEN** a consumer inspects commit-stage hooks in `.pre-commit-config.yaml`
- **THEN** an import-linter hook is present that runs the documented runner (or equivalent) against product
  `.importlinter`
- **AND** it fails closed when that config is missing in a product with `middleware/`

#### Scenario: Commit-stage includes uv audit

- **WHEN** a consumer inspects commit-stage hooks in `.pre-commit-config.yaml`
- **THEN** a uv-audit lockfile vulnerability hook is present
- **AND** it fails closed on findings except documented ignored advisory IDs

#### Scenario: Commit-stage includes gitleaks

- **WHEN** a consumer inspects commit-stage hooks in `.pre-commit-config.yaml`
- **THEN** a gitleaks secret-scan hook is present
- **AND** there is no ggshield secret-scan hook
- **AND** the gitleaks hook does not require `GITGUARDIAN_API_KEY`

#### Scenario: Missing product quality dep does not spawn-fail the gate

- **WHEN** a product checkout runs a synced vulture (or ruff/mypy/pylint/bandit/import-linter) hook or reusable
  code-quality step without that package in its `pyproject.toml`
- **THEN** the invocation still resolves the CLI from the fleet requirements pin
- **AND** it does not fail solely because the tool binary is absent from the project environment

#### Scenario: pytest stays product-owned

- **WHEN** a contributor inspects pre-push / reusable pytest invocations
- **THEN** they still use the project environment (`uv run pytest` or equivalent)
- **AND** pytest is not required to be listed in the fleet quality-tools requirements file

### Requirement: Commit-stage Helm lint with no-op when no charts

The shared pre-commit skeleton MUST include a **commit-stage** hook that lints product Helm charts. The hook MUST
discover chart roots as directories named `charts/<chart>/` that contain `Chart.yaml` (one path segment under
`charts/`). During a documented migration window the hook MUST also discover deprecated roots `helmchart/<chart>/` and
`helm/<chart>/` the same way. The fleet MUST NOT discover `helmcharts/` as a chart-root alias. When **no** such chart
exists, the hook MUST succeed without requiring the Helm CLI. When at least one chart exists, it MUST invoke `helm` from
`PATH` (Dev Container pin from `versions.env` `HELM_VERSION`) and run `helm lint` plus a default-values `helm template`
smoke render (same smoke as `reusable-helm-lint.yml` when `run_template` is true) on each discovered chart. The shared
Helm lint runner MUST accept an optional environment variable `HELM_VALUES_FILE` (path relative to the repository root).
When unset or empty, lint and template MUST use bare-chart behaviour (no `-f`), matching Feature-PR reusable behaviour
with empty `values_file`. When `HELM_VALUES_FILE` is non-empty, the runner MUST fail if that file is missing, and MUST
pass `-f` that path to `helm lint` and to `helm template` for each discovered chart. Missing `helm` while charts exist
MUST fail with guidance to use the Dev Container (or install the pinned Helm version). The hook MUST NOT treat
`check-yaml` as Helm validation; Go-templated chart templates MUST remain excluded from `check-yaml`. Repos without
charts (including this Devinfra tree) MUST remain a successful no-op. Documentation MUST state that **`charts/`** is the
canonical fleet chart root and that `helm/` / `helmchart/` are deprecated pending consumer renames.

#### Scenario: No chart directories is a no-op

- **WHEN** a contributor runs commit-stage quality (`pre-commit` / `scripts/quality-check.sh`) in a repo with no
  `charts/*/Chart.yaml`, `helmchart/*/Chart.yaml`, or `helm/*/Chart.yaml`
- **THEN** the Helm lint hook exits 0
- **AND** it does not fail solely because `helm` is missing from `PATH`

#### Scenario: Existing charts are linted and template-smoked

- **WHEN** a product checkout has at least one `charts/<chart>/Chart.yaml` (or, during migration,
  `helmchart/<chart>/Chart.yaml` or `helm/<chart>/Chart.yaml`)
- **AND** `helm` is on `PATH`
- **AND** `HELM_VALUES_FILE` is unset or empty
- **AND** the contributor runs commit-stage quality
- **THEN** each discovered chart is passed to `helm lint` without `-f`
- **AND** each chart is passed to `helm template` with chart default values (no `-f`)

#### Scenario: Legacy helm and helmchart roots still work during migration

- **WHEN** a product checkout has only `helmchart/<chart>/Chart.yaml` or only `helm/<chart>/Chart.yaml`
- **AND** `helm` is on `PATH`
- **AND** the contributor runs commit-stage quality
- **THEN** those charts are still discovered and linted
- **AND** documentation identifies those roots as deprecated

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

- **WHEN** `check-yaml` runs in a product repo that has `charts/`, `helm/`, or `helmchart/*/templates/*.yaml`
- **THEN** those template paths remain excluded
- **AND** Helm validation is the dedicated lint hook, not `check-yaml`

### Requirement: Helm lint local vs Feature-PR documentation

Documentation in this repository (at least `docs/quality.md`) MUST state that commit-stage quality runs Helm lint
locally via the shared hook, that Feature-PR CI still uses `reusable-helm-lint.yml` with a **separate** chart path
filter, and that IDE Helm extensions are optional and are **not** the gate. Documentation MUST state that the canonical
fleet chart root is **`charts/<chart>/`**, that `helm/` and `helmchart/` remain temporarily discovered as deprecated
roots, and that `helmcharts/` is not a supported alias. Documentation MUST state that optional overlay parity uses
`HELM_VALUES_FILE` locally and `values_file` on the Feature-PR reusable (same `-f` semantics when set; bare chart when
empty). Helm lint MUST NOT be required as an IDE save/lint extension to satisfy three-environment parity (named IDE
exception, same family as Bandit).

#### Scenario: Contributor reads local vs CI Helm lint

- **WHEN** a contributor opens `docs/quality.md` for Helm / chart quality
- **THEN** they learn local commit-stage lint is the shared hook
- **AND** they learn Feature-PR wiring remains the reusable with a separate detect-changes output
- **AND** they learn `charts/` is the canonical chart root (with deprecated dual discovery called out)
- **AND** they learn `HELM_VALUES_FILE` / `values_file` are the matching overlay knobs
- **AND** they learn IDE Helm tools are not a required third gate
