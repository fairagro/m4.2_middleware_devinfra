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
  pylint, **vulture**, **uv audit** (Python lockfile CVE gate), and markdownlint (aligned with the product API pattern).
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
synced whitelist file). The commit-stage **uv audit** hook MUST match the reusable code-quality uv-audit fail policy
(audit the project lockfile with `--frozen` or equivalent; fail on any reported vulnerability / adverse status except
IDs listed via the documented ignore mechanism).

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

#### Scenario: Commit-stage includes uv audit

- **WHEN** a consumer inspects commit-stage hooks in `.pre-commit-config.yaml`
- **THEN** a uv-audit lockfile vulnerability hook is present
- **AND** it fails closed on findings except documented ignored advisory IDs

### Requirement: Pre-push vs CI pytest scope is documented

Documentation (`docs/quality.md` and/or `docs/ci.md`) MUST state that synced pre-push pytest excludes `system_external`
and `system_local` by default, that the stage may take minutes for the remaining suite, that `SKIP=pytest` is an escape
hatch only, and that CI / intentional local runs of `system_*` use an explicit broader command (not a product fork of
`.pre-commit-config.yaml`). Docs MAY point at a follow-up for a shared pytest-marker plugin / coverage fragment SoT
without requiring that work in this change.

#### Scenario: Contributor reads pre-push pytest docs

- **WHEN** a contributor opens quality docs for pre-push
- **THEN** they learn which markers pre-push excludes
- **AND** they learn CI stays on a broader suite
- **AND** they learn `SKIP=pytest` is not the normal workflow

### Requirement: Templated container-structure-test runner

The repository MUST provide `scripts/run-container-structure-test.sh` that builds a Docker image via **Buildx Bake** and
runs `container-structure-test` against it. It MUST NOT fall back to a monolith `docker build -f` path. Bake target,
Bake file, image tag, and test definition paths MUST be configurable (arguments and/or environment variables) so product
repos can keep local values. When `CST_BAKE_TARGET` is unset and the checkout has **no product CST layout** — either no
`docker/` directory, or `docker/` without a `docker/container-structure-tests/` directory (e.g. shared Devinfra that
only ships `docker/Dockerfile.product-app.base` and examples) — the script MUST exit successfully with a clear skip
warning rather than failing the pre-push quality stage. Product repos that ship `docker/container-structure-tests/` MUST
require a Bake target / file and MUST still fail hard when those paths are wrong.

#### Scenario: Runner uses product parameters

- **WHEN** the script is invoked with product-specific Bake target, tag, and test paths
- **THEN** it builds that image via Bake and runs container-structure-test with those tests
- **AND** it does not hardcode another product’s paths as the only option
- **AND** it does not use monolith `docker build -f` as a fallback

#### Scenario: Devinfra without product CST layout skips

- **WHEN** the script runs without `CST_BAKE_TARGET`
- **AND** the repository has no `docker/` directory, **or** has `docker/` but no `docker/container-structure-tests/`
- **THEN** the script prints a skip warning and exits 0
- **AND** it does not attempt `docker buildx bake`

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
format/lint, Mypy, Pylint, Bandit, **vulture**, **uv audit**, markdownlint/Prettier where applicable, and pytest when
configured as a quality gate) MUST be runnable in all three environments:

1. **IDE** — workspace / extension settings that invoke the same tool binary family and the same shared config file(s)
2. **Git hooks** — pre-commit (commit stage) and, where the tool is a pre-push gate, the pre-push stage
3. **GitHub pipelines** — reusable or caller workflows that run the shared quality bar

**Documented IDE exceptions (named):** Bandit, **vulture**, and **uv audit** MUST gate via hooks and GitHub CI with a
matching fail bar, and MUST NOT require an IDE extension / workspace setting as a third gate.

For markdownlint/Prettier, GitHub pipelines MUST invoke the shared check scripts (e.g. `npm run format:md:check` /
`npm run lint:md`) in reusable code-quality (or an explicitly documented equivalent), not only commit-stage hooks.

For the same repository tree, the same toolchain pins (`versions.env` / `uv sync` / documented Node toolchain), and the
same target paths, the **pass/fail outcome and substantive findings** MUST match across those environments that gate the
tool. Divergent severity, rule sets, or config files between hooks and CI are forbidden unless a documented exception
exists (none by default for vulture/uv-audit beyond the IDE exceptions above).

Shared **config files** (e.g. `ruff.toml`, `mypy.ini`, `.pylintrc`, `.bandit`, markdownlint/Prettier configs) MUST be
the single source of truth for tool policy when the tool supports a syncable fragment. For **vulture** under the locked
fail policy (confidence 100, no whitelist file), matching hook and CI CLI args ARE the policy source of truth. For **uv
audit**, the documented runner invocation (frozen lockfile audit + shared ignore mechanism) IS the policy source of
truth.

Invocations (CLI, hook `entry`/`args`, CI steps, IDE settings) MUST pass at most: the path to the shared config file
when the tool does not auto-discover it, the analysis target path(s), documented path overlays, and for vulture the
shared confidence flag. They MUST NOT pass additional flags that restate or override policy already expressible in a
shared config file. They MUST NOT require post-sync hand-edits of synced `.pre-commit-config.yaml` for those overlays.

Documentation (`docs/quality.md` and/or Code Quality in `openspec/principles.global.md`) MUST state this three-
environment parity rule, the minimal-CLI rule, and the Bandit/vulture/uv-audit IDE exceptions. It MUST state that **uv
audit** is the primary Python lockfile/env CVE gate and **Trivy** remains the image/SBOM vulnerability gate
(`reusable-check`). It MUST state that **`UV_MALWARE_CHECK`** (or equivalent uv malware-check config) blocks known MAL
advisories at **sync/install** time and is not a substitute for `uv audit`.

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

#### Scenario: uv audit gates hooks and CI without IDE

- **WHEN** a contributor reads the environment parity table for uv audit
- **THEN** hooks and GitHub CI are listed as gates with the same fail bar
- **AND** IDE is documented as not required (named exception)
- **AND** docs distinguish uv audit (lock CVE gate) from Trivy (image gate) and from UV_MALWARE_CHECK (sync-time MAL)

### Requirement: Reusable code-quality runs vulture

The reusable code-quality workflow MUST run vulture against the configured Python package root with the same fail policy
as the commit-stage vulture hook (minimum confidence 100; no synced whitelist file). A failing vulture finding at that
policy MUST fail the job.

#### Scenario: CI vulture matches hook policy

- **WHEN** reusable code-quality runs with `skip` false
- **THEN** it executes vulture on the package root with minimum confidence 100
- **AND** a confidence-100 unused-code finding fails the workflow

### Requirement: uv audit lockfile gate and ignore overlay

The repository MUST provide a documented way to run **`uv audit`** against the project lockfile (`--frozen` or
equivalent) as the fleet primary Python lockfile/env vulnerability gate. Hooks and reusable CI MUST use the same
invocation and MUST fail on any vulnerability or adverse project status that is not ignored.

Accepted-risk ignores MUST use uv’s ID ignore flags (`--ignore` / `--ignore-until-fixed` or equivalent) applied via a
**product-owned overlay** (sync `overlays`, never wiped) and/or a thin shared runner that reads that overlay — MUST NOT
require post-sync edits to synced `.pre-commit-config.yaml`. Documentation MUST note that `uv audit` is preview /
experimental at the current uv pin and that there is **no** CRITICAL/HIGH-only severity filter.

#### Scenario: Frozen lockfile audit fails on findings

- **WHEN** commit-stage or reusable CI runs uv audit and the lockfile has a non-ignored advisory
- **THEN** the gate fails
- **AND** a clean lockfile (no findings / only ignored IDs) passes

#### Scenario: Product ignore overlay is not wiped by sync

- **WHEN** a product lists accepted advisory IDs in the documented overlay path
- **THEN** sync does not overwrite that overlay
- **AND** hooks and CI both honor those IDs without patching synced pre-commit YAML

### Requirement: UV malware check on fleet sync entrypoints

Fleet entrypoints that run `uv sync` for developer or quality bootstrap (at least reusable code-quality’s install step
and Dev Container post-create when it syncs) MUST enable uv’s malware check (`UV_MALWARE_CHECK=1` or equivalent
supported config) so known OSV MAL advisories abort sync before install. Documentation MUST state this is **install-time
malware blocking**, complementary to `uv audit`, and still preview/experimental at the current pin.

#### Scenario: Code-quality sync enables malware check

- **WHEN** reusable code-quality runs `uv sync` with `skip` false
- **THEN** the malware check is enabled for that sync
- **AND** a locked MAL advisory aborts the sync (gate fails)

#### Scenario: Docs describe malware check vs uv audit

- **WHEN** a contributor reads quality or CI docs for Python supply-chain gates
- **THEN** they learn UV_MALWARE_CHECK (or equivalent) runs at sync/install
- **AND** they learn `uv audit` remains the lockfile CVE gate

### Requirement: Markdown quality is gated in GitHub CI

Documentation of three-environment parity (`docs/quality.md` and related) MUST treat Prettier and markdownlint as gated
in **GitHub CI** via the reusable code-quality workflow (same shared configs and pass/fail outcome as IDE and hooks). It
MUST NOT present “commit-stage / docs scripts only” as a substitute for CI for those tools.

#### Scenario: Quality parity table shows CI for markdown

- **WHEN** a contributor reads the environment parity table in `docs/quality.md`
- **THEN** Prettier / markdownlint list GitHub CI as a real gate (not only commit-stage)
- **AND** the same shared config files are cited for IDE, hooks, and CI
