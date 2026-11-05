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
exclude Go-templated Helm chart templates under `helm/**/templates/` and `helmchart/**/templates/` (harmless when those
paths are absent) so product repos can adopt `.pre-commit-config.yaml` verbatim without post-sync hand-edits for Helm.

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

- **WHEN** `check-yaml` runs in a product repo that has `helm/` or `helmchart/*/templates/*.yaml`
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

## ADDED Requirements

### Requirement: Gitleaks CLI pin and install

The repository MUST pin gitleaks via `GITLEAKS_VERSION` in `versions.env` (Renovate-managed) and MUST provide an install
helper (e.g. `scripts/install-gitleaks.sh`) that places the pinned binary on `PATH` for Dev Container post-create and
CI. Commit-stage and reusable code-quality MUST use that installed binary (or an equivalent install-then-run path). The
install helper MUST fail closed when the pin is missing.

#### Scenario: Contributor has gitleaks after Dev Container create

- **WHEN** Dev Container post-create runs with a valid `GITLEAKS_VERSION` pin
- **THEN** `gitleaks` is on `PATH` at that pin
- **AND** the commit-stage gitleaks hook can invoke it without a SaaS API key

#### Scenario: Missing gitleaks pin fails install

- **WHEN** the install helper runs without `GITLEAKS_VERSION` set
- **THEN** it exits non-zero with a clear error
