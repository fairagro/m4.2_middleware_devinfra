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

### Requirement: Personal token store paths are per-product

Personal developer tokens (`GH_TOKEN`, `GITGUARDIAN_API_KEY`, and equivalents) MUST use `/commandhistory/tokens.env`
inside a Dev Container. On the host, the store MUST be `~/.config/<git-repo-name>/tokens.env` where `<git-repo-name>` is
the GitHub repository name derived from the clone's `origin` remote (fallback: basename of the git toplevel). Token
stores MUST NOT be shared across different products or Dev Containers. Host paths MUST NOT require a `PRODUCT_SLUG`
environment variable.

#### Scenario: Two product Dev Containers on one machine

- **WHEN** a developer uses both the API and harvester Dev Containers on the same host
- **THEN** each product uses its own host token file under `~/.config/<git-repo-name>/tokens.env`
- **AND** in-container both still read `/commandhistory/tokens.env` from that product's own volume

#### Scenario: Host clone derives repo name without PRODUCT_SLUG

- **WHEN** `dev-tokens.sh` runs on a host clone without `/commandhistory`
- **AND** the clone has an `origin` remote (or a resolvable git toplevel)
- **THEN** it uses `~/.config/<git-repo-name>/tokens.env` without requiring `PRODUCT_SLUG`

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
