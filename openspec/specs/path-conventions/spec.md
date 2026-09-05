# path-conventions Specification

## Purpose

Defines the shared naming and path conventions that product repos and later Devinfra extracts MUST follow for personal
tokens, Dev Container volumes, and the product package root—so sync and shared scripts do not encode conflicting names.

## Requirements

### Requirement: Conventions document exists and is indexed

The repository MUST provide `docs/conventions.md` documenting path and naming conventions, and the root `README.md` Docs
index MUST link to it.

#### Scenario: Contributor looks up shared path rules

- **WHEN** a contributor opens the root `README.md` Docs section
- **THEN** they find a link to `docs/conventions.md`
- **AND** that document contains the token, volume, and package-root conventions

### Requirement: Personal token store is Dev Container volume path

Personal developer tokens (`GH_TOKEN`, `GITGUARDIAN_API_KEY`, and equivalents) MUST use `/commandhistory/tokens.env`
inside the Linux Dev Container. Token stores MUST NOT be shared across different products' Dev Containers (isolation is
via each product's own bashhistory volume). Helpers MUST NOT implement a host `~/.config/…` token path (unsupported
outside the Dev Container).

#### Scenario: Two product Dev Containers on one machine

- **WHEN** a developer uses both the API and harvester Dev Containers on the same host
- **THEN** in-container each reads `/commandhistory/tokens.env` from that product's own bashhistory volume
- **AND** the two containers do not share token state through a common host config directory

### Requirement: Docker volume names follow a product-slug pattern

Named Docker volumes for bash history and (when used) `gh` config MUST follow `<product-slug>-bashhistory` and
`<product-slug>-gh-config`. Shared Devinfra files MUST NOT hardcode another product's volume `source=` name; product
overlays own those names. The conventions document MUST include a slug table for the known repos.

#### Scenario: Sync does not collide volumes

- **WHEN** shared Dev Container fragments are synced into multiple product repos
- **THEN** each product's overlay (or documented slug) supplies a distinct volume `source=` name
- **AND** two products on one machine do not share the same bashhistory volume by convention

### Requirement: Product package root is middleware/

Product application packages MUST live under a repo-relative `middleware/` tree (`middleware/<package>/`). Shared
quality tooling MAY target `middleware/` as a whole. This Devinfra repository MUST NOT contain product `middleware/`
packages.

#### Scenario: Quality tooling scope

- **WHEN** shared quality or pre-commit config refers to product code
- **THEN** it uses the `middleware/` package root (or a documented per-repo override)
- **AND** this Devinfra repo remains without a product `middleware/` tree
