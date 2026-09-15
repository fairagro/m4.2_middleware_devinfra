## ADDED Requirements

### Requirement: Root gitignore is allowlisted

`docs/synced-paths.yaml` MUST list root `.gitignore` under `allow` so product consumers receive the shared fleet ignore
baseline after sync. Products MUST NOT treat root `.gitignore` as a standing sync exclude or as a product-owned fork.

#### Scenario: .gitignore on allowlist

- **WHEN** a contributor inspects the product sync path allowlist
- **THEN** `.gitignore` appears under `allow`
- **AND** they learn product-only ignore lines belong in nested `.gitignore` files, not in the synced root file

### Requirement: Nested gitignore overlays for product-only paths

Documentation (`docs/sync.md`) MUST state that product-specific ignore paths (demo output, helm TLS scratch, etc.) MUST
live in nested `.gitignore` files under product-owned trees. Sync MUST NOT overwrite those nested files. Root
`.gitignore` MUST remain verbatim after sync (no post-sync append of product lines).

#### Scenario: Product delta uses nested ignore

- **WHEN** a product needs to ignore a path that is not fleet-common (e.g. `dev_environment/demo_output`)
- **THEN** docs direct placing that rule in a nested `.gitignore` (e.g. under `dev_environment/`)
- **AND** the synced root `.gitignore` is left unchanged in the product checkout
