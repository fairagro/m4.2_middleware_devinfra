## MODIFIED Requirements

### Requirement: Shared pre-commit skeleton

The repository MUST provide a root `.pre-commit-config.yaml` that defines:

- **Commit-stage** hooks covering at least: trailing-whitespace / YAML or TOML hygiene, ggshield, ruff, mypy, bandit,
  pylint, **vulture**, and markdownlint (aligned with the product API pattern).
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
synced whitelist file).

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

### Requirement: Three-environment quality parity

Every shared quality tool that gates commits or CI for this repository or for synced product consumers (at least: Ruff
format/lint, Mypy, Pylint, Bandit, **vulture**, markdownlint/Prettier where applicable, and pytest when configured as a
quality gate) MUST be runnable in all three environments:

1. **IDE** — workspace / extension settings that invoke the same tool binary family and the same shared config file(s)
2. **Git hooks** — pre-commit (commit stage) and, where the tool is a pre-push gate, the pre-push stage
3. **GitHub pipelines** — reusable or caller workflows that run the shared quality bar

**Documented IDE exceptions (named):** Bandit and **vulture** MUST gate via hooks and GitHub CI with a matching fail
bar, and MUST NOT require an IDE extension / workspace setting as a third gate (same class of exception as existing
Bandit documentation).

For markdownlint/Prettier, GitHub pipelines MUST invoke the shared check scripts (e.g. `npm run format:md:check` /
`npm run lint:md`) in reusable code-quality (or an explicitly documented equivalent), not only commit-stage hooks.

For the same repository tree, the same toolchain pins (`versions.env` / `uv sync` / documented Node toolchain), and the
same target paths, the **pass/fail outcome and substantive findings** MUST match across those environments that gate
the tool. Divergent severity, rule sets, or config files between hooks and CI are forbidden unless a documented
exception exists (none by default for vulture beyond the IDE exception above).

Shared **config files** (e.g. `ruff.toml`, `mypy.ini`, `.pylintrc`, `.bandit`, markdownlint/Prettier configs) MUST be
the single source of truth for tool policy when the tool supports a syncable fragment. For **vulture** under the locked
fail policy (confidence 100, no whitelist file), matching hook and CI CLI args ARE the policy source of truth.

Invocations (CLI, hook `entry`/`args`, CI steps, IDE settings) MUST pass at most: the path to the shared config file
when the tool does not auto-discover it, the analysis target path(s), documented path overlays, and for vulture the
shared confidence flag. They MUST NOT pass additional flags that restate or override policy already expressible in a
shared config file. They MUST NOT require post-sync hand-edits of synced `.pre-commit-config.yaml` for those overlays.

Documentation (`docs/quality.md` and/or Code Quality in `openspec/principles.global.md`) MUST state this three-
environment parity rule, the minimal-CLI rule, and the Bandit/vulture IDE exceptions.

#### Scenario: Same tree fails or passes consistently

- **WHEN** a contributor runs the shared quality bar via IDE-integrated checks (where applicable), via pre-commit (or
  `quality-check.sh`), and via the reusable code-quality GitHub workflow against the same tree and pins
- **THEN** each gating environment uses the same shared policy for that tool
- **AND** the gate outcome (pass vs fail on policy findings) is the same across hooks and CI for tools that gate both
- **AND** Prettier/markdownlint participate in the reusable workflow gate, not only commit-stage

#### Scenario: Invocations do not restate config policy on the CLI

- **WHEN** a consumer inspects shared pre-commit entries, reusable CI quality steps, and IDE tool settings for a gated
  quality tool that has a shared config file
- **THEN** those invocations reference the shared config file path (when required) and target paths / allowed path
  overlays only
- **AND** they do not add CLI or IDE flags that duplicate policy already defined in that config file

#### Scenario: Vulture gates hooks and CI without IDE

- **WHEN** a contributor reads the environment parity table for vulture
- **THEN** hooks and GitHub CI are listed as gates with the same fail bar
- **AND** IDE is documented as not required (named exception with Bandit)

## ADDED Requirements

### Requirement: Reusable code-quality runs vulture

The reusable code-quality workflow MUST run vulture against the configured Python package root with the same fail
policy as the commit-stage vulture hook (minimum confidence 100; no synced whitelist file). A failing vulture finding
at that policy MUST fail the job.

#### Scenario: CI vulture matches hook policy

- **WHEN** reusable code-quality runs with `skip` false
- **THEN** it executes vulture on the package root with minimum confidence 100
- **AND** a confidence-100 unused-code finding fails the workflow
