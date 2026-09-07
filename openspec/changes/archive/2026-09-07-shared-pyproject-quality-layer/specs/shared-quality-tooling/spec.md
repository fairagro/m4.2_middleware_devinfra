# shared-quality-tooling Delta

## ADDED Requirements

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
