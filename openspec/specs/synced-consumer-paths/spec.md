# synced-consumer-paths Specification

## Purpose

Defines the single allowlist of Devinfra-canonical paths that product consumers must not hand-edit after sync, and that
`/review-fixer` must treat as read-only in consumer checkouts (except documented product-local overlays).

## Requirements

### Requirement: Synced paths allowlist document

The repository MUST provide `docs/synced-paths.yaml` as the **sole** canonical allowlist of paths synced from Devinfra
into product repos. The YAML MUST expose an `allow` list (paths/globs to sync), an `exclude` list (never copy), and MAY
document `overlays` (product-local exceptions). The same file MUST be the source of truth for (1) paths consumers MUST
NOT hand-edit after sync, (2) `/review-fixer` read-only synced trees in product checkouts, and (3) product-repo sync
automation path selection. There MUST NOT be a second hand-maintained sync path list. The `allow` list MUST cover
concrete paths or globs for all shipped shared surfaces (including AI stack, Renovate artifacts, personal-token helpers,
quality scripts/hooks, Dev Container shared fragments, `docker/Dockerfile.product-app.base`,
`.github/workflows/codeql.yml`, and related docs). `exclude` / `overlays` MUST cover at least: product `middleware/`,
`openspec/specs/**`, `openspec/changes/**`, reusable CI workflow YAML (`reusable-*.yml`), and documented overlays (e.g.
`docs/surface-quality-bar.md`, `openspec/principles.md`, `AGENTS.md`). The root `README.md` Docs index MUST link to this
YAML. Sync of this allowlist MUST NOT overwrite product-local overlay files.

#### Scenario: Contributor looks up what not to edit after sync

- **WHEN** a contributor opens `docs/synced-paths.yaml` in Devinfra or after sync into a product repo
- **THEN** they find the allowlist of Devinfra-canonical synced paths
- **AND** they find named product-local overlay paths that remain editable in consumers

#### Scenario: README indexes the allowlist

- **WHEN** a contributor reads the root `README.md` Docs section
- **THEN** they find a link to `docs/synced-paths.yaml`

#### Scenario: Renovate artifacts are on the allowlist

- **WHEN** a contributor checks whether Renovate config or workflow may be hand-edited in a product repo after sync
- **THEN** `renovate.json` and `.github/workflows/renovate.yml` appear on the synced allowlist
- **AND** they learn shared Renovate changes land in Devinfra first

#### Scenario: CodeQL workflow is on the allowlist

- **WHEN** a contributor checks whether `.github/workflows/codeql.yml` may be hand-edited in a product repo after sync
- **THEN** that path appears on the synced allowlist
- **AND** they learn shared CodeQL changes land in Devinfra first

#### Scenario: Allowlist is the only sync path SoT

- **WHEN** sync automation or a contributor looks for “what files are copied to products”
- **THEN** `docs/synced-paths.yaml` is the only hand-maintained path list
- **AND** hard excludes for OpenSpec specs trees and `middleware/` are documented there

### Requirement: Workspace extensions recommendations are allowlisted

`docs/synced-paths.yaml` MUST list `.vscode/extensions.json` under `allow` so products receive the same VS Code / Cursor
extension recommendations as Devinfra after sync. The recommendations set MUST stay aligned with the shared Dev
Container extension list (see `shared-devcontainer-base`).

#### Scenario: extensions.json on allowlist

- **WHEN** a contributor inspects the product sync path allowlist
- **THEN** `.vscode/extensions.json` appears under `allow`
- **AND** it is not listed as a standing sync exclude

### Requirement: Node markdown toolchain manifests are allowlisted

`docs/synced-paths.yaml` MUST list root `package.json` and `package-lock.json` under `allow` so product consumers
receive the same npm scripts and pins used by commit-stage markdown hooks and reusable code-quality CI. Products MUST
NOT treat those manifests as standing sync excludes.

#### Scenario: package.json on allowlist

- **WHEN** a contributor inspects the product sync path allowlist
- **THEN** `package.json` and `package-lock.json` appear under `allow`
- **AND** they learn markdown CI/hooks adopt those files via sync from Devinfra

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
