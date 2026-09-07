# Shared Python quality config layer (issue #28 MVP)

## Why

Product repos duplicate large root `pyproject.toml` `[tool.*]` blocks (ruff/mypy/pylint/…). Fixes drift across three
repos. Issue #28 also asked for a shared app Dockerfile; explore locked **A2** — this change delivers only the **quality
config layer**; Dockerfile work is deferred to a sub-issue (unified stages, shared base Dockerfile with ARGs, thin local
last stage).

## What Changes

- Add Devinfra-owned **fragment config files** for shared Python quality tools (**B2**): at least `ruff.toml` and
  mypy/pylint equivalents extracted from the product API pattern (middleware-oriented), ready for #13 sync.
- Keep product-local concerns out of those fragments: `[project]`, uv workspace, and typically pytest/coverage stay in
  each product’s root `pyproject.toml`.
- Document adoption: which files sync, what stays local, that `scripts/ai/pyproject.toml` is Devinfra package metadata
  and is **not** part of the product quality sync set.
- Document that smoke adoption in a product repo is **out of this PR** (**D1**); #13 applies the files.
- **Out of scope here:** product app Dockerfile base + last-stage split (follow-up sub-issue); editing product repos;
  removing `scripts/ai/pyproject.toml`.

## Capabilities

### New Capabilities

- `shared-python-quality-config`: Canonical fragment files and docs for shared ruff/mypy/pylint (and related) config
  synced into product repos without replacing product root `pyproject.toml` project/uv sections.

### Modified Capabilities

- `shared-quality-tooling`: Clarify that Python tool config for products is supplied via the fragment files (not by
  expanding Devinfra’s own root `pyproject.toml` into a product-shaped monolith), and point docs/hooks expectations at
  those paths when synced.

## Impact

- New config files under an agreed path (see design); `docs/quality.md` (+ README pointer if needed).
- Pre-commit skeleton may need hook args/config path notes so synced consumers resolve `ruff.toml` / mypy config.
- Sub-issue for Dockerfile (relation `sub-of #28`) records **C**: unify stages → shared base Dockerfile with ARGs +
  product-local last stage.
