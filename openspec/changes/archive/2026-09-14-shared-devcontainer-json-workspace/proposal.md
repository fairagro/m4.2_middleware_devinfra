## Why

Fleet rule (issue #65): either Dev Container entry files are generic enough for **verbatim** product sync, or they stay
explicitly product-owned — post-sync hand-edits of a synced blob are an emergency only. Today docs still describe a
“thin `devcontainer.json` overlay” while sync excludes JSON and Compose; products keep near-copies that re-state `name`
/ `workspaceFolder` / volume sources / bind paths. We lock **Option A**: shared **`devcontainer.json` and
`docker-compose.yml`**, common in-container path `/workspace`, and a distinct window title via
`${localWorkspaceFolderBasename}`.

## What Changes

- Make `.devcontainer/devcontainer.json` **verbatim-generic**: `workspaceFolder` `/workspace`, Docker volume `source=`
  names and window/`name` from `${localWorkspaceFolderBasename}` (no hardcoded product strings); shared `PATH` /
  extensions / postCreate only — no product `MYPYPATH` / `CST_*` / `postStart` in JSON.
- Make `.devcontainer/docker-compose.yml` **verbatim-generic**: bind `..:/workspace:cached` (same for all repos); shared
  build-args from `versions.env`. Put both files on the sync **allow** list (remove from `exclude`).
- Repo-specific container env (`MYPYPATH`, `CST_*`, …) MUST live outside those blobs: optional product-owned
  `.devcontainer/product.env` referenced from shared Compose with `required: false` (file not synced), and/or existing
  CI / hook env inputs — never by patching synced JSON or Compose after sync.
- **BREAKING** (product adopt): drop thin-overlay docs; after sync, products stop owning JSON/Compose copies; migrate
  bind to `/workspace`; move product env into `product.env` (or CI-only); drop JSON `postStart` / multi-postCreate
  deltas (align with shared postCreate / #58).
- Update `docs/devcontainer.md`, `docs/sync.md`, `docs/conventions.md`, and `shared-devcontainer-base`. Starship may
  show directory `workspace`; identity via window `name`, Git, and venv/package (prompt polish out of MVP).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `shared-devcontainer-base`: Replace thin-overlay / product-owned JSON+Compose story with verbatim-shared JSON and
  Compose (`/workspace` + basename `name`/volumes); optional non-synced `product.env` for repo env; sync allowlist
  alignment.

## Impact

- Devinfra: `.devcontainer/devcontainer.json`, `.devcontainer/docker-compose.yml`, `docs/synced-paths.yaml`, Dev
  Container / sync / conventions docs, OpenSpec `shared-devcontainer-base`.
- Product repos (after sync): adopt synced JSON+Compose; add local `.devcontainer/product.env` when `MYPYPATH`/`CST_*`
  are needed in the container; remove hand-maintained overlay copies and bind-path forks.
