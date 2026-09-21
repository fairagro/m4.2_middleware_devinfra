## MODIFIED Requirements

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

## ADDED Requirements

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
