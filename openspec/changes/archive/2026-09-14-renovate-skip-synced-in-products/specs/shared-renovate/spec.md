# shared-renovate Delta

## ADDED Requirements

### Requirement: Product Renovate skips Devinfra-synced dependency SoT

The shared `renovate.json` MUST disable dependency updates in the three product repositories
(`fairagro/m4.2_advanced_middleware_api`, `fairagro/m4.2_sql_to_arc`, `fairagro/m4.2_middleware_harvester`) for paths
and packages owned by Devinfra and delivered via sync (#13), including at least: `versions.env`, `.python-version`,
`docker/Dockerfile.product-app.base`, `.devcontainer/Dockerfile`, `renovate.json`, `.github/workflows/renovate.yml`, and
the BuildKit frontend package `docker/dockerfile`. Those updates MUST continue to run in Devinfra. Product-local
managers (e.g. pep621 under `middleware/`, product last-stage image tags other than the disabled frontend package) MUST
remain enabled in product repos.

#### Scenario: Product Renovate does not open versions.env CLI bump PRs

- **WHEN** Renovate runs in a product repo with the shared config
- **AND** newer GitHub-release CLI pins exist for entries in `versions.env`
- **THEN** it does not open a PR that only updates that synced `versions.env` file

#### Scenario: Product Renovate does not bump docker/dockerfile syntax tags

- **WHEN** Renovate runs in a product repo with the shared config
- **AND** a product Dockerfile contains `# syntax=docker/dockerfile:…`
- **THEN** it does not open a PR solely to bump that frontend package
