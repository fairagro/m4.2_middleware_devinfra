# shared-python-quality-config Specification

## Purpose

Canonical fragment configuration files for shared Python quality tools (ruff, mypy, pylint, and closely related) so m4.2
product repos sync those files from Devinfra instead of duplicating large `[tool.*]` blocks in root `pyproject.toml`.

## Requirements

### Requirement: Shared Ruff fragment exists

The repository MUST provide a root-level `ruff.toml` (or `.ruff.toml`) that encodes the shared Ruff lint and format
policy for product `middleware/` trees. The file MUST be suitable to sync into product repos at the same relative path
and MUST NOT encode Devinfra-only package layout as the sole target in a way that breaks product `middleware/` usage.

#### Scenario: Contributor opens shared ruff config

- **WHEN** a contributor opens the shared Ruff fragment in this repository
- **THEN** shared line-length, lint selections, and format settings for middleware products are present
- **AND** the path is documented as part of the product sync set

### Requirement: Shared Mypy fragment exists

The repository MUST provide a shared Mypy config file at a documented root-relative path that products can sync.
Product-specific path overrides MUST be documented as product hook/CI env or args overlays (e.g. `MYPYPATH`, pylint
`--source-roots`), not as `[tool.mypy]` / `[tool.pylint.*]` in product `pyproject.toml` when shared invocations use
`--config-file mypy.ini` / `--rcfile .pylintrc`, and not as edits to the synced fragments. The shared file MUST be
usable for type-checking `middleware/` in product checkouts after sync.

#### Scenario: Shared mypy config targets middleware

- **WHEN** a product adopts the shared Mypy fragment without replacing its root `[project]` / uv workspace
- **THEN** Mypy can be run against `middleware/` using that fragment
- **AND** adoption docs state that path overlays use product hook/CI env or args (not `pyproject` under `--config-file`)

### Requirement: Shared Pylint fragment exists

The repository MUST provide a shared Pylint config file at a documented root-relative path aligned with the shared Ruff
policy (avoid duplicate noisy checks). It MUST be syncable into product repos at the same relative path.

#### Scenario: Shared pylint config is syncable

- **WHEN** sync copies the Pylint fragment into a product repo
- **THEN** pre-commit or CLI Pylint can use that file without requiring product-specific Devinfra paths

### Requirement: Quality config adoption documentation

Documentation in this repository MUST list the fragment files in the sync set, state that product root `pyproject.toml`
keeps `[project]`, uv workspace, and (unless later unified) pytest/coverage locally, and state that
`scripts/ai/pyproject.toml` is Devinfra `m42-ai` package metadata and MUST NOT be treated as product quality sync
content. Documentation MUST state that Mypy/Pylint path overlays belong on product hook/CI env or args because shared
invocations use `--config-file mypy.ini` / `--rcfile .pylintrc` (so product `[tool.mypy]` / `[tool.pylint.*]` are
ignored), and MUST NOT instruct editing synced fragments for those paths. Documentation MUST state that Dockerfile
sharing is out of this capability’s MVP and point at the follow-up issue. Documentation MUST state that first product
adoption smoke may happen via sync (#13) rather than in this change.

#### Scenario: Contributor reads quality docs for fragments

- **WHEN** a contributor opens the quality documentation for shared Python config
- **THEN** they learn which fragment paths to sync
- **AND** they learn what remains in product `pyproject.toml`
- **AND** they learn path overlays for Mypy/Pylint go on product hook/CI env or args
- **AND** they learn `scripts/ai/pyproject.toml` is excluded from that sync set

### Requirement: Fragment config is the only policy surface

Shared Ruff, Mypy, and Pylint fragment files MUST carry the full shared policy for those tools. Shared and product
invocations (IDE, pre-commit / pre-push, GitHub quality workflows, `quality-check.sh`) MUST NOT pass command-line or IDE
settings that restate fragment-expressible policy. Allowed extras are limited to: `--config` / `--config-file` /
`--rcfile` (or IDE equivalent pointing at the fragment), target paths such as `middleware/`, and documented
product-local path overlays (`MYPYPATH`, pylint `--source-roots`, and equivalents) that MUST NOT be edited into synced
fragments.

#### Scenario: Mypy invocation stays minimal

- **WHEN** shared hooks, CI, or docs show a Mypy command for product `middleware/`
- **THEN** the command uses `--config-file mypy.ini` (or auto-discovery of that fragment) plus target paths
- **AND** it does not add CLI flags that duplicate settings already present in `mypy.ini`
