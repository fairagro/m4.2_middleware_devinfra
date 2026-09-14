## ADDED Requirements

### Requirement: Shared Pyright / basedpyright fragment exists

The repository MUST provide a root-level `pyrightconfig.json` suitable to sync into product repos at the same relative
path. The shared file MUST set analysis to the workspace root `.venv` (`venvPath` / `venv`), MUST set `stubPath` to
`stubs` for product-local third-party stubs (keeping silence out of synced `mypy.ini`), MUST include `scripts/ai/src` in
`extraPaths` for the shared `m42-ai` workspace member, and MUST include the documented common excludes (`node_modules`,
`__pycache__`, dot-directories, `.venv` / `venv`). The shared file MUST NOT list product `middleware/` or other
product-only package paths (editable `uv` installs resolve those). Product-only excludes (e.g. `dev_environment`) MUST
NOT be required in the shared blob.

#### Scenario: Contributor opens shared pyrightconfig

- **WHEN** a contributor opens root `pyrightconfig.json` in this repository
- **THEN** `venv` / `venvPath`, `stubPath: stubs`, `extraPaths` including `scripts/ai/src`, and the common excludes are
  present
- **AND** no product `middleware/` package path appears in `extraPaths`

#### Scenario: Fragment is on the sync allowlist

- **WHEN** a contributor inspects the product sync path allowlist
- **THEN** `pyrightconfig.json` is listed for verbatim sync into product repos

## MODIFIED Requirements

### Requirement: Quality config adoption documentation

Documentation in this repository MUST list the fragment files in the sync set (including `pyrightconfig.json`), state
that product root `pyproject.toml` keeps `[project]`, uv workspace, and (unless later unified) pytest/coverage locally,
and state that `scripts/ai/pyproject.toml` is Devinfra `m42-ai` package metadata and MUST NOT be treated as product
quality sync content. Documentation MUST state that Mypy/Pylint path overlays belong on process env / reusable CI inputs
because shared invocations use `--config-file mypy.ini` / `--rcfile .pylintrc` (so product `[tool.mypy]` /
`[tool.pylint.*]` are ignored), MUST NOT instruct editing synced fragments for those paths, and MUST NOT instruct
post-sync hand-edits of synced `.pre-commit-config.yaml` for path overlays. Documentation MUST state that basedpyright /
Pylance analysis uses the synced `pyrightconfig.json`, that product third-party stubs live under `stubs/` via
`stubPath`, and that product package paths MUST NOT be added to the synced Pyright config (rely on editable installs).
Documentation MUST state that Dockerfile sharing is out of this capability’s MVP and point at the follow-up issue.
Documentation MUST state that first product adoption smoke may happen via sync (#13) rather than in this change.

#### Scenario: Contributor reads quality docs for fragments

- **WHEN** a contributor opens the quality documentation for shared Python config
- **THEN** they learn which fragment paths to sync (including `pyrightconfig.json`)
- **AND** they learn what remains in product `pyproject.toml`
- **AND** they learn path overlays for Mypy/Pylint go on env / CI inputs (not synced pre-commit YAML patches)
- **AND** they learn `scripts/ai/pyproject.toml` is excluded from that sync set
- **AND** they learn basedpyright uses synced `pyrightconfig.json` with product stubs under `stubs/` and no product
  package paths in that file
