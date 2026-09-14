## ADDED Requirements

### Requirement: Shared incomplete stubs for arctrl and fable_library

The repository MUST provide incomplete type stub packages under `stubs/arctrl/` and `stubs/fable_library/` suitable to
sync into product repos (same relative paths). Stubs MAY use `__getattr__ -> Any` (and sparse leaf modules as needed) so
imports resolve without enumerating every symbol. The repository MUST provide `stubs/README.md` stating: (1) arctrl and
fable_library stubs are fleet-shared via sync; (2) owslib / rdflib stubs stay product-local when needed; (3) one-off
untyped libs use `# type: ignore[import-untyped]` on the import rather than new stub packages; (4) products MUST put
`stubs` on `MYPYPATH` for hooks/CI and rely on synced `pyrightconfig.json` `stubPath` for basedpyright; (5) products
MUST NOT add `[mypy-arctrl*]` / fable module overrides to synced `mypy.ini` and MUST NOT keep import-untyped ignores for
packages covered by these stubs after sync.

#### Scenario: Shared stub trees exist

- **WHEN** a contributor inspects `stubs/arctrl/` and `stubs/fable_library/` in this repository
- **THEN** incomplete package stubs are present for both
- **AND** `stubs/README.md` documents fleet vs product-local vs one-off silence

#### Scenario: Stubs are on the sync allowlist

- **WHEN** a contributor inspects the product sync path allowlist
- **THEN** `stubs/arctrl/**`, `stubs/fable_library/**`, and `stubs/README.md` are listed for verbatim sync

## MODIFIED Requirements

### Requirement: Quality config adoption documentation

Documentation in this repository MUST list the fragment files in the sync set (including `pyrightconfig.json` and the
shared `stubs/arctrl` / `stubs/fable_library` trees), state that product root `pyproject.toml` keeps `[project]`, uv
workspace, and (unless later unified) pytest/coverage locally, and state that `scripts/ai/pyproject.toml` is Devinfra
`m42-ai` package metadata and MUST NOT be treated as product quality sync content. Documentation MUST state that
Mypy/Pylint path overlays belong on process env / reusable CI inputs because shared invocations use
`--config-file mypy.ini` / `--rcfile .pylintrc` (so product `[tool.mypy]` / `[tool.pylint.*]` are ignored), MUST NOT
instruct editing synced fragments for those paths, and MUST NOT instruct post-sync hand-edits of synced
`.pre-commit-config.yaml` for path overlays. Documentation MUST state that basedpyright / Pylance analysis uses the
synced `pyrightconfig.json`, that product third-party stubs live under `stubs/` via `stubPath`, and that product package
paths MUST NOT be added to the synced Pyright config (rely on editable installs). Documentation MUST state that shared
arctrl / fable_library stubs live under synced `stubs/` and that `MYPYPATH` MUST include `stubs` so mypy finds them;
MUST NOT instruct `[mypy-arctrl*]` / fable overrides in synced `mypy.ini`. Documentation MUST state that Dockerfile
sharing is out of this capability’s MVP and point at the follow-up issue. Documentation MUST state that first product
adoption smoke may happen via sync (#13) rather than in this change.

#### Scenario: Contributor reads quality docs for fragments

- **WHEN** a contributor opens the quality documentation for shared Python config
- **THEN** they learn which fragment paths to sync (including `pyrightconfig.json` and shared `stubs/arctrl` /
  `stubs/fable_library`)
- **AND** they learn what remains in product `pyproject.toml`
- **AND** they learn path overlays for Mypy/Pylint go on env / CI inputs (not synced pre-commit YAML patches)
- **AND** they learn `scripts/ai/pyproject.toml` is excluded from that sync set
- **AND** they learn basedpyright uses synced `pyrightconfig.json` with product stubs under `stubs/` and no product
  package paths in that file
- **AND** they learn `MYPYPATH` must include `stubs` for shared arctrl / fable stubs without mypy.ini module overrides
