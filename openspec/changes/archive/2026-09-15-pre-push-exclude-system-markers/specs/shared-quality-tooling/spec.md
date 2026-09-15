## MODIFIED Requirements

### Requirement: Shared pre-commit skeleton

The repository MUST provide a root `.pre-commit-config.yaml` that defines:

- **Commit-stage** hooks covering at least: trailing-whitespace / YAML or TOML hygiene, ggshield, ruff, mypy, bandit,
  pylint, and markdownlint (aligned with the product API pattern).
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

## ADDED Requirements

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
