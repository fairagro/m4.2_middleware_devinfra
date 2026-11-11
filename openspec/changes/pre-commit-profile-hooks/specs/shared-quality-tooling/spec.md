## MODIFIED Requirements

### Requirement: Shared pre-commit skeleton

The repository MUST provide **profile-scoped pre-commit fragments** and a **compose** step that writes each consumer’s
root `.pre-commit-config.yaml`. Fragments MUST cover at least:

- **foundation** — trailing-whitespace / YAML or TOML hygiene (with vendor-skill and Helm-template excludes as today),
  **gitleaks**, prettier-md, markdownlint, commitlint, commit-path-check
- **python-product** — ruff, mypy, bandit, pylint, **vulture**, **import-linter**, **uv audit**, and **pre-push**
  `pytest` + container-structure-test (CST via `scripts/run-container-structure-test.sh`)
- **gitops** — commit-stage **helm-lint** (actionlint / kubeconform MAY be added in later changes)

Python-product consumers MUST compose **foundation ∪ python-product ∪ gitops** so behavior matches the former single
blob (including helm-lint). Infrastructure MUST compose **foundation** and MAY include **gitops**; it MUST NOT receive
python-product hooks. Devinfra’s own root `.pre-commit-config.yaml` MUST be the composed product-union result (or
equivalent) so local hooks stay coherent.

The pre-push `pytest` hook (python-product fragment) MUST invoke pytest with marker expression
`-m "not system_external and not system_local"` (or equivalent), print a short duration / `SKIP=pytest` notice, and MUST
NOT be Infra’s required gate. Reusable CI MUST NOT silently inherit that pre-push marker filter as its only suite.

Python-oriented hooks MUST target the `middleware/` package root. Config MUST exclude vendor agent skill trees under
`.agents/skills/` (at least `gh`, `docker`, `hadolint`, `uv`, and `scan-secrets` when present). Shared `check-yaml` MUST
exclude Go-templated Helm templates under `charts/**/templates/` and, during migration, `helm/**/templates/` and
`helmchart/**/templates/`. The fleet MUST NOT treat `helmcharts/` as a supported chart-root alias in that exclude list.

Vulture / import-linter / uv-audit / gitleaks / quality-CLI pin rules from the prior single-skeleton contract remain in
force for the fragments that carry those hooks (confidence 100; product `.importlinter`; `--frozen` uv audit; gitleaks
fail-closed without SaaS key; ruff/mypy/pylint/bandit/vulture/import-linter via `scripts/run-quality-cli.sh` pins;
gitleaks from `versions.env`).

Documentation (`docs/quality.md`) MUST describe fragments, compose, the consumer matrix, and migration for the three
python-product repos. Products MUST NOT need post-sync hand-edits of the composed root solely for Helm excludes or the
locked hook map.

#### Scenario: Pre-commit config lists both stages

- **WHEN** a python-product consumer inspects the composed root `.pre-commit-config.yaml`
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
- **AND** products do not need to patch the composed `.pre-commit-config.yaml` solely for that exclude

#### Scenario: Commit-stage includes vulture

- **WHEN** a python-product consumer inspects commit-stage hooks in the composed root config
- **THEN** a vulture unused-code hook is present for `middleware/`
- **AND** it uses minimum confidence 100 without a synced whitelist file

#### Scenario: Commit-stage includes import-linter

- **WHEN** a python-product consumer inspects commit-stage hooks in the composed root config
- **THEN** an import-linter hook is present that runs the documented runner against product `.importlinter`
- **AND** it fails closed when that config is missing in a product with `middleware/`

#### Scenario: Commit-stage includes uv audit

- **WHEN** a python-product consumer inspects commit-stage hooks in the composed root config
- **THEN** a uv-audit lockfile vulnerability hook is present
- **AND** it fails closed on findings except documented ignored advisory IDs

#### Scenario: Commit-stage includes gitleaks

- **WHEN** a consumer with the foundation fragment inspects commit-stage hooks in the composed root config
- **THEN** a gitleaks secret-scan hook is present
- **AND** there is no ggshield secret-scan hook
- **AND** the gitleaks hook does not require `GITGUARDIAN_API_KEY`

#### Scenario: Missing product quality dep does not spawn-fail the gate

- **WHEN** a product checkout runs a synced vulture (or ruff/mypy/pylint/bandit/import-linter) hook or reusable
  code-quality step without that package in its `pyproject.toml`
- **THEN** the gate still invokes the CLI via the synced pin helper instead of failing only because the binary is
  missing from the project env

#### Scenario: pytest stays product-owned

- **WHEN** a contributor inspects pre-push / reusable pytest invocations
- **THEN** they still use the project environment (`uv run pytest` or equivalent)
- **AND** pytest is not required to be listed in the fleet quality-tools requirements file

#### Scenario: Infra composed config omits python-product hooks

- **WHEN** infrastructure composes foundation (and optionally gitops) without python-product
- **THEN** the composed root has no `middleware/`-scoped ruff/mypy/bandit/pylint/vulture/import-linter hooks and no
  pre-push pytest/CST hooks
- **AND** foundation hygiene hooks (and gitops helm-lint when included) remain present

### Requirement: Commit-stage Helm lint with no-op when no charts

The **gitops** pre-commit fragment MUST include a **commit-stage** hook that lints product Helm charts (composed into
consumers that select gitops). The hook MUST discover chart roots as directories named `charts/<chart>/` that contain
`Chart.yaml` (one path segment under `charts/`). During a documented migration window the hook MUST also discover
deprecated roots `helmchart/<chart>/` and `helm/<chart>/` the same way. The fleet MUST NOT discover `helmcharts/` as a
chart-root alias. When **no** such chart exists, the hook MUST succeed without requiring the Helm CLI. When at least one
chart exists, it MUST invoke `helm` from `PATH` (Dev Container pin from `versions.env` `HELM_VERSION`) and run
`helm lint` plus a default-values `helm template` smoke render (same smoke as `reusable-helm-lint.yml` when
`run_template` is true) on each discovered chart. The shared Helm lint runner MUST accept an optional environment
variable `HELM_VALUES_FILE` (path relative to the repository root). When unset or empty, lint and template MUST use
bare-chart behaviour (no `-f`), matching Feature-PR reusable behaviour with empty `values_file`. When `HELM_VALUES_FILE`
is non-empty, the runner MUST fail if that file is missing, and MUST pass `-f` that path to `helm lint` and to
`helm template` for each discovered chart. Missing `helm` while charts exist MUST fail with guidance to use the Dev
Container (or install the pinned Helm version). The hook MUST NOT treat `check-yaml` as Helm validation; Go-templated
chart templates MUST remain excluded from `check-yaml`. Repos without charts (including this Devinfra tree) MUST remain
a successful no-op. Documentation MUST state that **`charts/`** is the canonical fleet chart root and that `helm/` /
`helmchart/` are deprecated pending consumer renames.

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

## ADDED Requirements

### Requirement: Pre-commit profile fragments are the editable SoT

Devinfra MUST store editable pre-commit hook definitions as profile fragments (paths under a documented directory such
as `.pre-commit.d/` or equivalent), not as three unrelated hand-maintained root configs. A documented compose command
(script or checked-in generator) MUST merge the selected fragments into root `.pre-commit-config.yaml` for the active
consumer matrix. Hand-editing only the generated root without updating fragments MUST be documented as incorrect.
Compose MUST be deterministic (stable hook order within the locked map).

#### Scenario: Contributor edits a fragment then composes

- **WHEN** a maintainer changes a hook in the foundation fragment and runs the documented compose for python-product
- **THEN** the root `.pre-commit-config.yaml` reflects that change
- **AND** docs name the compose command and fragment paths

#### Scenario: No dual SoT

- **WHEN** a contributor looks for where to change shared hook policy
- **THEN** docs direct them to the profile fragments (and compose), not to maintaining a divergent root-only copy
