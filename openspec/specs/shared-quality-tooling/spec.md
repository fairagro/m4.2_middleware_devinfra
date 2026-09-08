# shared-quality-tooling Specification

## Purpose

Shared commit-stage and pre-push quality tooling (scripts, pre-commit skeleton, bandit, templated
container-structure-test runner) that product repos can sync with minimal local tweaks.

## Requirements

### Requirement: Commit-stage quality helper scripts

The repository MUST provide `scripts/quality-check.sh` and `scripts/quality-fix.sh` that run the shared **commit-stage**
pre-commit hooks only (MUST NOT run the pre-push hook stage). Check MUST be non-mutating validation; fix MUST apply
auto-fixes where hooks support them.

#### Scenario: Contributor runs quality-check

- **WHEN** a contributor runs `scripts/quality-check.sh` with a configured `.pre-commit-config.yaml`
- **THEN** commit-stage hooks run
- **AND** pre-push stage hooks (pytest / container-structure-test) do not run

#### Scenario: Contributor runs quality-fix

- **WHEN** a contributor runs `scripts/quality-fix.sh`
- **THEN** commit-stage hooks run in a mode that applies supported auto-fixes
- **AND** pre-push stage hooks do not run

### Requirement: Shared pre-commit skeleton

The repository MUST provide a root `.pre-commit-config.yaml` that defines:

- **Commit-stage** hooks covering at least: trailing-whitespace / YAML or TOML hygiene, ggshield, ruff, mypy, bandit,
  pylint, and markdownlint (aligned with the product API pattern).
- **Pre-push stage** hooks for `pytest` and container-structure-test that invoke
  `scripts/run-container-structure-test.sh`.

Python-oriented hooks MUST target the `middleware/` package root (per path conventions). Config MUST exclude vendor
agent skill trees that are pinned under `.agents/skills/` (at least `gh`, `docker`, `hadolint`, `uv`, and `scan-secrets`
when present) from hooks that walk the tree (or equivalent exclude lists).

#### Scenario: Pre-commit config lists both stages

- **WHEN** a consumer inspects `.pre-commit-config.yaml`
- **THEN** commit-stage and pre-push stages are both present
- **AND** the pre-push CST entry calls the shared runner script

#### Scenario: Vendor skills are excluded

- **WHEN** commit-stage hooks that scan files run
- **THEN** paths under pinned vendor skill directories (e.g. `.agents/skills/gh/`, `docker/`, `hadolint/`, `uv/`) are
  excluded

### Requirement: Templated container-structure-test runner

The repository MUST provide `scripts/run-container-structure-test.sh` that builds a Docker image and runs
`container-structure-test` against it. Dockerfile path, image tag, and test definition paths MUST be configurable
(arguments and/or environment variables) so product repos can keep local values. When the configured Dockerfile path is
missing and the checkout has **no product CST layout** — either no `docker/` directory, or `docker/` without both a
default `docker/Dockerfile` and a `docker/container-structure-tests/` directory (e.g. shared Devinfra that only ships
`docker/Dockerfile.product-app.base` and examples) — the script MUST exit successfully with a clear skip warning rather
than failing the pre-push quality stage. Product repos that ship a product `docker/` layout MUST still fail hard when
the configured Dockerfile path is wrong.

#### Scenario: Runner uses product parameters

- **WHEN** the script is invoked with product-specific Dockerfile, tag, and test paths
- **THEN** it builds that image and runs container-structure-test with those tests
- **AND** it does not hardcode another product’s paths as the only option

#### Scenario: Devinfra without product CST layout skips

- **WHEN** the script runs with the default Dockerfile path and that file is missing
- **AND** the repository has no `docker/` directory, **or** has `docker/` but neither `docker/Dockerfile` nor
  `docker/container-structure-tests/`
- **THEN** the script prints a skip warning and exits 0
- **AND** it does not attempt `docker build`

### Requirement: Bandit and markdownlint config files

The repository MUST provide a root `.bandit` suitable for `bandit -c`. It MUST provide or retain `.markdownlint.json`,
`.markdownlintignore`, and `.markdownlint-cli2.jsonc` consistent with Prettier and vendor excludes.

#### Scenario: Bandit config exists

- **WHEN** a consumer runs bandit with `-c .bandit` against `middleware/`
- **THEN** the shared `.bandit` file is present at the repo root

### Requirement: Documentation of hook install boundaries

Documentation (README and/or `docs/`) MUST state that commit-stage installation is
`pre-commit install --hook-type pre-commit` (performed by shared `scripts/devcontainer-post-create.sh` on Dev Container
create, and runnable manually after clone), and that the pre-push **git** hook (pre-commit pre-push stage only) is
installed via `scripts/setup-git-hooks.sh` from the shared git-hooks extract (also invoked from that postCreate). Manual
`uv run pre-commit run --hook-stage pre-push` remains valid without that git hook. Documentation MUST NOT require Git
LFS for the shared pre-push quality path.

#### Scenario: Contributor reads install docs

- **WHEN** a contributor opens the quality / README docs for this tooling
- **THEN** they learn how to install the commit-stage hook
- **AND** they learn pre-push git-hook install is `./scripts/setup-git-hooks.sh` (wired from postCreate on the Dev
  Container path)

### Requirement: Python tool config via syncable fragments

Shared Python quality **tool configuration** for product repos MUST be provided as dedicated fragment files owned in
this repository (Ruff, Mypy, Pylint — see `shared-python-quality-config`), not by treating this repository’s root
`pyproject.toml` as a drop-in replacement for product root `pyproject.toml`. The pre-commit skeleton and quality docs
MUST be consistent with those fragment paths after sync (hooks discover or pass the documented config files). Existing
`.bandit` and markdownlint configs remain separate fragment-style files as already required.

#### Scenario: Pre-commit expects fragment configs after sync

- **WHEN** a product repo has synced the shared Ruff/Mypy/Pylint fragments and the shared pre-commit skeleton
- **THEN** commit-stage Ruff/Mypy/Pylint hooks can resolve configuration without requiring product `[tool.ruff]` blocks
  copied from an old monolith `pyproject.toml`
- **AND** documentation states that product `[project]` / uv workspace sections stay local

### Requirement: Three-environment quality parity

Every shared quality tool that gates commits or CI for this repository or for synced product consumers (at least: Ruff
format/lint, Mypy, Pylint, Bandit, markdownlint/Prettier where applicable, and pytest when configured as a quality gate)
MUST be runnable in all three environments:

1. **IDE** — workspace / extension settings that invoke the same tool binary family and the same shared config file(s)
2. **Git hooks** — pre-commit (commit stage) and, where the tool is a pre-push gate, the pre-push stage
3. **GitHub pipelines** — reusable or caller workflows that run the shared quality bar

For the same repository tree, the same toolchain pins (`versions.env` / `uv sync` / documented Node toolchain), and the
same target paths, the **pass/fail outcome and substantive findings** MUST match across those three environments.
Divergent severity, rule sets, or config files between IDE, hooks, and CI are forbidden unless a documented exception
exists (none by default).

Shared **config files** (e.g. `ruff.toml`, `mypy.ini`, `.pylintrc`, `.bandit`, markdownlint/Prettier configs) MUST be
the single source of truth for tool policy. Invocations (CLI, hook `entry`/`args`, CI steps, IDE settings) MUST pass at
most: the path to the shared config file when the tool does not auto-discover it, the analysis target path(s), and
product-local path overlays that cannot live in synced fragments (e.g. `MYPYPATH`, pylint `--source-roots`). They MUST
NOT pass additional command-line (or IDE-equivalent) flags that restate or override policy already expressible in the
shared config file (line length, rule selects, ignore lists, severity thresholds, Python version pins, and similar).

Documentation (`docs/quality.md` and/or Code Quality in `openspec/principles.global.md`) MUST state this three-
environment parity rule and the minimal-CLI rule.

#### Scenario: Same tree fails or passes consistently

- **WHEN** a contributor runs the shared quality bar via IDE-integrated checks, via pre-commit (or `quality-check.sh`),
  and via the reusable code-quality GitHub workflow against the same tree and pins
- **THEN** each environment uses the same shared config file(s) for that tool
- **AND** the gate outcome (pass vs fail on policy findings) is the same across the three

#### Scenario: Invocations do not restate config policy on the CLI

- **WHEN** a consumer inspects shared pre-commit entries, reusable CI quality steps, and IDE tool settings for a gated
  quality tool
- **THEN** those invocations reference the shared config file path (when required) and target paths / allowed path
  overlays only
- **AND** they do not add CLI or IDE flags that duplicate policy already defined in that config file
