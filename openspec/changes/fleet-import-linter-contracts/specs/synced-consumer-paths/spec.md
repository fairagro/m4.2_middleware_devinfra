## ADDED Requirements

### Requirement: Import-linter baseline allowlisted; product overlay is an overlay

`docs/synced-paths.yaml` MUST list the synced import-linter **baseline** path under `allow`. The product import-linter
**overlay** path MUST be listed under `overlays` (and MUST NOT be wiped by sync). Documentation (`docs/sync.md` and/or
`docs/quality.md`) MUST name both paths.

#### Scenario: Baseline on allowlist

- **WHEN** a contributor inspects the product sync path allowlist
- **THEN** the import-linter baseline config path appears under `allow`

#### Scenario: Overlay never overwritten

- **WHEN** a contributor inspects sync overlays documentation
- **THEN** the product import-linter overlay path is listed as a product-owned overlay
- **AND** sync does not overwrite that path
