# shared-python-quality-config Delta

## Purpose

Canonical fragment configuration files for shared Python quality tools (ruff, mypy, pylint, and closely related) so m4.2
product repos sync those files from Devinfra instead of duplicating large `[tool.*]` blocks in root `pyproject.toml`.

## ADDED Requirements

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
Product-specific path overrides (e.g. extra `mypy_path` entries) MAY remain documented as local overlays; the shared
file MUST be usable for type-checking `middleware/` in product checkouts after sync.

#### Scenario: Shared mypy config targets middleware

- **WHEN** a product adopts the shared Mypy fragment without replacing its root `[project]` / uv workspace
- **THEN** Mypy can be run against `middleware/` using that fragment
- **AND** adoption docs state what may stay product-local

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
content. Documentation MUST state that Dockerfile sharing is out of this capability’s MVP and point at the follow-up
issue. Documentation MUST state that first product adoption smoke may happen via sync (#13) rather than in this change.

#### Scenario: Contributor reads quality docs for fragments

- **WHEN** a contributor opens the quality documentation for shared Python config
- **THEN** they learn which fragment paths to sync
- **AND** they learn what remains in product `pyproject.toml`
- **AND** they learn `scripts/ai/pyproject.toml` is excluded from that sync set
