# synced-consumer-paths Delta

## MODIFIED Requirements

### Requirement: Synced paths allowlist document

The repository MUST provide `docs/synced-paths.yaml` as the **sole** canonical allowlist of paths synced from
Devinfra into product repos. The YAML MUST expose an `allow` list (paths/globs to sync), an `exclude` list (never
copy), and MAY document `overlays` (product-local exceptions). The same file MUST be the source of truth for (1) paths
consumers MUST NOT hand-edit after sync, (2) `/review-fixer` read-only synced trees in product checkouts, and (3)
product-repo sync automation path selection. There MUST NOT be a second hand-maintained sync path list. The `allow`
list MUST cover concrete paths or globs for all shipped
shared surfaces (including AI stack, Renovate artifacts, personal-token helpers, quality scripts/hooks, Dev Container
shared fragments, `docker/Dockerfile.product-app.base`, and related docs). `exclude` / `overlays` MUST cover at least:
product `middleware/`, `openspec/specs/**`, `openspec/changes/**`, reusable CI workflow YAML (`reusable-*.yml`), and
documented overlays (e.g. `docs/surface-quality-bar.md`, `openspec/principles.md`, `AGENTS.md`). The root `README.md`
Docs index MUST link to this YAML. Sync of this allowlist MUST NOT overwrite product-local overlay files.

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

#### Scenario: Allowlist is the only sync path SoT

- **WHEN** sync automation or a contributor looks for “what files are copied to products”
- **THEN** `docs/synced-paths.yaml` is the only hand-maintained path list
- **AND** hard excludes for OpenSpec specs trees and `middleware/` are documented there
