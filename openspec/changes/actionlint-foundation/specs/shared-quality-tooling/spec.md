## ADDED Requirements

### Requirement: Actionlint CLI pin and install

The repository MUST pin actionlint via `ACTIONLINT_VERSION` in `versions.env` (Renovate-managed) and MUST provide an
install helper (e.g. `scripts/install-actionlint.sh`) that places the pinned binary on `PATH` for Dev Container image
builds / create paths and CI. Commit-stage hooks and reusable code-quality MUST use that installed binary (or an
equivalent install-then-run path from the same pin). The install helper MUST fail closed when the pin is missing. Docs
MUST state that the same `ACTIONLINT_VERSION` applies to local hooks and GitHub Actions (no second pin via pre-commit
`rev`).

#### Scenario: Contributor has actionlint after Dev Container rebuild

- **WHEN** a contributor rebuilds the Dev Container with a valid `ACTIONLINT_VERSION` pin
- **THEN** `actionlint` is on `PATH` at that pin
- **AND** the commit-stage actionlint hook can invoke it

#### Scenario: Missing actionlint pin fails install

- **WHEN** the install helper runs without `ACTIONLINT_VERSION` set
- **THEN** it exits non-zero with a clear error

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
exclude Go-templated Helm templates under `charts/**/templates/` and, during migration, `helm/**/templates/` and
`helmchart/**/templates/`. The fleet MUST NOT treat `helmcharts/` as a supported chart-root alias in that exclude list.

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

- **WHEN** `check-yaml` runs in a product repo that has `charts/`, `helm/`, or `helmchart/*/templates/*.yaml`
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
