## ADDED Requirements

### Requirement: Shared import-linter baseline and product overlay

The repository MUST provide a syncable **import-linter baseline** configuration for product `middleware/` trees that
encodes the mechanically enforceable core of the fleet Import policy:

- `root_package` (or equivalent) targeting `middleware`
- `exclude_type_checking_imports = True` so `TYPE_CHECKING` edges are not treated as runtime graph edges
- at least one **acyclic_siblings** (or equivalent) contract with ancestor `middleware` so sibling packages under
  `middleware` must not form import cycles

The baseline MUST NOT invent product-specific layer names (`layers` / `forbidden` / `independence` for product
packages). Those MUST live in a **product-owned overlay** file that sync MUST NOT overwrite (listed under
`docs/synced-paths.yaml` `overlays` or an equivalent documented non-allowlisted path).

Hooks and reusable CI MUST run import-linter such that the baseline always applies and, when the overlay file is
present, its contracts are included (via a documented merge/wrapper if the upstream CLI accepts only one config file).
When the overlay is absent, the baseline alone MUST still run and fail on cycle violations.

Documentation MUST state that **pydeps** (if mentioned) is optional/local visualization only and MUST NOT be a CI or
pre-commit fail gate. Documentation MUST state which Import-policy rules remain outside import-linter (module-level
placement, no relative imports, no `sys.path` mutation, no lazy imports solely to break cycles) and stay principles /
other tools / code-review judgment.

#### Scenario: Baseline encodes acyclic middleware siblings

- **WHEN** a consumer inspects the synced import-linter baseline
- **THEN** it targets `middleware`, excludes TYPE_CHECKING imports from the graph, and includes an acyclic-siblings
  contract for `middleware`
- **AND** it does not define product-specific layer package lists

#### Scenario: Overlay is product-owned

- **WHEN** a contributor inspects the sync allowlist / overlays documentation for import-linter
- **THEN** the baseline path is synced
- **AND** the product overlay path is documented as never overwritten by sync

#### Scenario: Gate runs baseline with optional overlay

- **WHEN** commit-stage or reusable CI runs import-linter
- **THEN** the baseline contracts are always checked
- **AND** if the product overlay exists, its contracts are checked in the same run
