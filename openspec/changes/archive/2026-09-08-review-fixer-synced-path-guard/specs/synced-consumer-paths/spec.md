# synced-consumer-paths Delta

## Purpose

Defines the single allowlist of Devinfra-canonical paths that product consumers must not hand-edit after sync, and that
`/review-fixer` must treat as read-only in consumer checkouts (except documented product-local overlays).

## ADDED Requirements

### Requirement: Synced paths allowlist document

The repository MUST provide `docs/synced-paths.global.md` as the canonical allowlist of paths synced from Devinfra into
product repos that consumers MUST NOT hand-edit. The document MUST list (or glob) at least: shared AI review policy and
surface-bar global map, fixer skill/command/prompt entrypoints, first-party and vendor agent skills under
`.agents/skills/` that sync ships, `scripts/ai/**`, personal-token helpers (`scripts/dev-tokens.sh`,
`scripts/set-dev-tokens.sh`, `scripts/bin/gh`, `scripts/bin/git`), `openspec/principles.global.md`, and other Wave A /
sync-manifest paths as they exist. It MUST name documented **product-local overlay** exceptions (e.g.
`docs/surface-quality-bar.md`, `openspec/principles.md`, `AGENTS.md`) that MAY be edited in consumers. The root
`README.md` Docs index MUST link to this file. Sync of this allowlist MUST NOT overwrite product-local overlay files.

#### Scenario: Contributor looks up what not to edit after sync

- **WHEN** a contributor opens `docs/synced-paths.global.md` in Devinfra or after sync into a product repo
- **THEN** they find the allowlist of Devinfra-canonical synced paths
- **AND** they find named product-local overlay paths that remain editable in consumers

#### Scenario: README indexes the allowlist

- **WHEN** a contributor reads the root `README.md` Docs section
- **THEN** they find a link to `docs/synced-paths.global.md`
