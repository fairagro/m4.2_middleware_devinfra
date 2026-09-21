## ADDED Requirements

### Requirement: Import-linter baseline allowlisted; product overlay is an overlay

`docs/synced-paths.yaml` MUST list the synced import-linter baseline **`.importlinter.global`** under `allow`. The
product import-linter overlay **`.importlinter`** MUST be listed under `overlays` (and MUST NOT be wiped by sync).
Documentation (`docs/sync.md` and/or `docs/quality.md`) MUST name both paths and MUST follow the fleet
synced-`.global` + product-local naming pair.

#### Scenario: Baseline on allowlist

- **WHEN** a contributor inspects the product sync path allowlist
- **THEN** `.importlinter.global` appears under `allow`

#### Scenario: Overlay never overwritten

- **WHEN** a contributor inspects sync overlays documentation
- **THEN** `.importlinter` is listed as a product-owned overlay
- **AND** sync does not overwrite that path

### Requirement: Synced `.global` + product overlay naming

When a shared Devinfra file has a product-specific companion that sync must not overwrite, the repository MUST use the
pair **`*.global` / `*.global.*` (synced SoT on `allow`)** and **the same basename without `.global` (product overlay on
`overlays`)**. Examples MUST include at least `openspec/principles.global.md` + `openspec/principles.md`,
`docs/surface-quality-bar.global.md` + `docs/surface-quality-bar.md`, and `.importlinter.global` + `.importlinter`.
Documentation in `openspec/principles.global.md` and `docs/sync.md` MUST state this naming rule. Alternate suffixes such
as `.product` MUST NOT be used for this split.

#### Scenario: Contributor looks up shared vs product file names

- **WHEN** a contributor reads principles or sync docs for overlay naming
- **THEN** they learn synced SoT files use a `.global` stem and product companions drop `.global`
- **AND** they see import-linter cited as `.importlinter.global` + `.importlinter`
