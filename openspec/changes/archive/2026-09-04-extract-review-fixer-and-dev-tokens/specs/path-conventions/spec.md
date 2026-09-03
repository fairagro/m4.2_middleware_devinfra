# Path Conventions — Delta

## MODIFIED Requirements

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
