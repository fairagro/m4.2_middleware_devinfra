## ADDED Requirements

### Requirement: Synced `.global` + product overlay naming is documented

`openspec/principles.global.md` MUST document the fleet naming rule for splitting a shared synced file from a
product-specific companion: synced SoT uses a **`.global`** stem (`*.global` / `*.global.*`) on the sync `allow` list;
the product companion uses the **same basename without `.global`** and is listed under sync `overlays` (never
overwritten). The document MUST cite examples including `principles.global.md` / `principles.md`,
`surface-quality-bar.global.md` / `surface-quality-bar.md`, and `.importlinter.global` / `.importlinter`. It MUST forbid
inventing alternate suffixes such as `.product` for this split.

#### Scenario: Contributor reads principles for overlay naming

- **WHEN** a contributor opens `openspec/principles.global.md` looking for how shared vs product files are named
- **THEN** they find the synced-`.global` + product-local pair rule with the import-linter and principles examples
- **AND** they learn not to use a `.product` suffix for that split
