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
Product-specific path overrides MUST be documented as process env / reusable CI inputs (e.g. `MYPYPATH`, workflow
`mypy_path`), not as `[tool.mypy]` / `[tool.pylint.*]` in product `pyproject.toml` when shared invocations use
`--config-file mypy.ini` / `--rcfile .pylintrc`, not as edits to synced fragments, and not as post-sync patches to
synced `.pre-commit-config.yaml`. The shared file MUST be usable for type-checking `middleware/` in product checkouts
after sync.

#### Scenario: Shared mypy config targets middleware

- **WHEN** a product adopts the shared Mypy fragment without replacing its root `[project]` / uv workspace
- **THEN** Mypy can be run against `middleware/` using that fragment
- **AND** adoption docs state that path overlays use env / CI inputs (not `pyproject` under `--config-file`, not synced
  pre-commit YAML edits)

### Requirement: Shared Pylint fragment exists

The repository MUST provide a shared Pylint config file at a documented root-relative path aligned with the shared Ruff
policy (avoid duplicate noisy checks). It MUST be syncable into product repos at the same relative path.

#### Scenario: Shared pylint config is syncable

- **WHEN** sync copies the Pylint fragment into a product repo
- **THEN** pre-commit or CLI Pylint can use that file without requiring product-specific Devinfra paths

### Requirement: Shared Pyright / basedpyright fragment exists

The repository MUST provide a root-level `pyrightconfig.json` suitable to sync into product repos at the same relative
path. The shared file MUST set analysis to the workspace root `.venv` (`venvPath` / `venv`), MUST include
`scripts/ai/src` in `extraPaths` for the shared `m42-ai` workspace member, and MUST include the documented common
excludes (`node_modules`, `__pycache__`, dot-directories, `.venv` / `venv`). The shared file MUST NOT require a synced
`stubs/` tree or `stubPath` pointing at fleet stubs. The shared file MUST NOT list product `middleware/` or other
product-only package paths (editable `uv` installs resolve those). Product-only excludes (e.g. `dev_environment`) MUST
NOT be required in the shared blob.

#### Scenario: Contributor opens shared pyrightconfig

- **WHEN** a contributor opens root `pyrightconfig.json` in this repository
- **THEN** `venv` / `venvPath`, `extraPaths` including `scripts/ai/src`, and the common excludes are present
- **AND** no product `middleware/` package path appears in `extraPaths`
- **AND** the file does not require a Devinfra-synced `stubs/` directory

#### Scenario: Fragment is on the sync allowlist

- **WHEN** a contributor inspects the product sync path allowlist
- **THEN** `pyrightconfig.json` is listed for verbatim sync into product repos

### Requirement: Fleet untyped arctrl and fable_library silenced in tool config

The repository MUST NOT provide or sync a `stubs/` directory (including `stubs/README.md` or arctrl/fable stub trees).
Untyped fleet imports of `arctrl` / `fable_library` MUST be silenced in synced tool fragments instead:

- `mypy.ini`: `[mypy-arctrl*]` / `[mypy-fable_library*]` with `ignore_missing_imports = True`
- `.pylintrc`: `ignored-modules` including `arctrl` and `fable_library`
- `ruff.toml`: document that Ruff does not gate missing third-party imports; keep `known-third-party` for isort
  classification of those packages
- `pyrightconfig.json`: MUST NOT rely on shared stubs; MAY set `typeCheckingMode` so basedpyright is not a second type
  gate alongside mypy

Products MUST NOT add duplicate arctrl/fable silences to product `pyproject.toml` when synced fragments already cover
them. One-off untyped libs (not arctrl/fable) MAY use `# type: ignore[import-untyped]` on the import. Sync allowlist
MUST NOT list any `stubs/**` paths.

#### Scenario: No stubs directory in Devinfra

- **WHEN** a contributor inspects the repository root
- **THEN** there is no `stubs/` directory synced from Devinfra

#### Scenario: Tool fragments silence fleet deps

- **WHEN** a contributor opens synced `mypy.ini`, `.pylintrc`, and `ruff.toml`
- **THEN** mypy module overrides and pylint `ignored-modules` cover `arctrl` / `fable_library`
- **AND** ruff documents that it does not emit third-party missing-import diagnostics for those packages

#### Scenario: Sync allowlist excludes stubs

- **WHEN** a contributor inspects the product sync path allowlist
- **THEN** no `stubs/**` path is listed

### Requirement: Quality config adoption documentation

Documentation in this repository MUST list the fragment files in the sync set (including `pyrightconfig.json`, without
any `stubs/**` paths), state that product root `pyproject.toml` keeps `[project]`, uv workspace, and (unless later
unified) pytest/coverage locally, and state that `scripts/ai/pyproject.toml` is Devinfra `m42-ai` package metadata and
MUST NOT be treated as product quality sync content. Documentation MUST state that Mypy/Pylint path overlays belong on
process env / reusable CI inputs because shared invocations use `--config-file mypy.ini` / `--rcfile .pylintrc` (so
product `[tool.mypy]` / `[tool.pylint.*]` are ignored), MUST NOT instruct editing synced fragments for those paths, and
MUST NOT instruct post-sync hand-edits of synced `.pre-commit-config.yaml` for path overlays. Documentation MUST state
that basedpyright / Pylance analysis uses the synced `pyrightconfig.json` and that product package paths MUST NOT be
added to that file (rely on editable installs). Documentation MUST state that untyped fleet `arctrl` / `fable_library`
imports are silenced in synced `mypy.ini` / `.pylintrc` (and documented for Ruff), not via stub packages. Documentation
MUST state that Dockerfile sharing is out of this capability’s MVP and point at the follow-up issue. Documentation MUST
state that first product adoption smoke may happen via sync (#13) rather than in this change.

#### Scenario: Contributor reads quality docs for fragments

- **WHEN** a contributor opens the quality documentation for shared Python config
- **THEN** they learn which fragment paths to sync (including `pyrightconfig.json`, without a synced `stubs/` tree)
- **AND** they learn what remains in product `pyproject.toml`
- **AND** they learn path overlays for Mypy/Pylint go on env / CI inputs (not synced pre-commit YAML patches)
- **AND** they learn `scripts/ai/pyproject.toml` is excluded from that sync set
- **AND** they learn basedpyright uses synced `pyrightconfig.json` with no product package paths in that file
- **AND** they learn fleet arctrl/fable silence is in mypy/pylint (and ruff docs), not stub packages

### Requirement: Fragment config is the only policy surface

Shared Ruff, Mypy, and Pylint fragment files MUST carry the full shared policy for those tools. Shared and product
invocations (IDE, pre-commit / pre-push, GitHub quality workflows, `quality-check.sh`) MUST NOT pass command-line or IDE
settings that restate fragment-expressible policy. Allowed extras are limited to: `--config` / `--config-file` /
`--rcfile` (or IDE equivalent pointing at the fragment), target paths such as `middleware/`, and documented
product-local path overlays (`MYPYPATH`, pylint `--source-roots`, and equivalents) supplied via process env or CI inputs
that MUST NOT be edited into synced fragments or into synced `.pre-commit-config.yaml`.

#### Scenario: Mypy invocation stays minimal

- **WHEN** shared hooks, CI, or docs show a Mypy command for product `middleware/`
- **THEN** the command uses `--config-file mypy.ini` (or auto-discovery of that fragment) plus target paths
- **AND** it does not add CLI flags that duplicate settings already present in `mypy.ini`

### Requirement: Shared vulture unused-code gate

The repository MUST provide a fleet **vulture** unused-code gate for product `middleware/` trees. Invocations (commit-
stage pre-commit and reusable code-quality CI) MUST use the same fail policy: minimum confidence **100** and **no**
synced vulture whitelist / ignore fragment. Policy MUST live in the shared hook and CI entries (same args), not in a
product-local `pyproject` `[tool.vulture]` table that sync would overwrite inconsistently.

Documentation MUST state that false positives at confidence 100 are handled in product code (`# noqa` / delete / use the
symbol), not by expanding a Devinfra whitelist file in this change. Dynamic attributes, `__all__`, and pytest fixtures
that still fail at 100 MUST be fixed or noqa’d in the product — not by lowering fleet confidence in a one-off product
fork of the synced pre-commit blob.

#### Scenario: Vulture gate uses confidence 100 without whitelist file

- **WHEN** a consumer inspects the shared vulture pre-commit entry and the reusable code-quality vulture step
- **THEN** both invoke vulture against `middleware/` (or the documented package root input) with minimum confidence 100
- **AND** neither depends on a synced vulture whitelist file for the fail policy

#### Scenario: Docs describe FP handling without a fleet whitelist

- **WHEN** a contributor reads quality docs for vulture
- **THEN** they learn confidence 100 and no synced whitelist
- **AND** they learn to fix or `# noqa` in product code rather than patching synced hook YAML after sync

### Requirement: Product-owned import-linter config

The repository MUST **not** sync an import-linter **config** file (no `.importlinter.global`). Product repos with a `middleware/` tree
MUST own a root **`.importlinter`** that includes the fleet-required mechanical Import-policy settings documented in
`docs/quality.md`:

- `exclude_type_checking_imports = True`
- an **acyclic_siblings** (or equivalent) contract with ancestor `middleware`
- `root_package` or `root_packages` appropriate to a regular package or PEP 420 portions (no path-mutating
  `middleware/__init__.py`)

Product-specific `layers` / `forbidden` / `independence` contracts MUST live in that same product `.importlinter`. Hooks
and reusable CI MUST invoke
`bash scripts/run-quality-cli.sh lint-imports --config .importlinter` (or an
equivalent documented command using the same pin file and config path). Missing `.importlinter` in a product with
`middleware/` MUST fail closed. Documentation MUST state that **pydeps** is optional/local visualization only and MUST
NOT be a CI or pre-commit fail gate, and which Import-policy rules remain outside import-linter.

#### Scenario: Docs list required product settings

- **WHEN** a contributor reads `docs/quality.md` for import-linter
- **THEN** they see the required `.importlinter` settings every product must adopt
- **AND** they learn there is no synced `.importlinter.global` (optional thin `run-import-linter.sh` only)

#### Scenario: Gate uses product config

- **WHEN** commit-stage or reusable CI runs import-linter in a product repo with `middleware/`
- **THEN** it runs `lint-imports` against the product `.importlinter`
- **AND** a missing `.importlinter` fails the gate

#### Scenario: PEP 420 portions without path mutation

- **WHEN** a product uses a PEP 420 `middleware` namespace
- **THEN** docs direct listing portion names in `root_packages`
- **AND** docs forbid adding a path-mutating `middleware/__init__.py`
