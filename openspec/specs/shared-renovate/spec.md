# shared-renovate Specification

## Purpose

Defines the canonical Renovate configuration, per-repo GitHub Actions workflow, and documentation so Devinfra and synced
product consumers use Renovate for dependency version updates instead of Dependabot version updates.

## Requirements

### Requirement: Canonical renovate.json in Devinfra

The repository MUST provide a root `renovate.json` (or equivalent Renovate config file) that enables managers needed for
shared and product layouts (at least dockerfile, devcontainer, pep621, github-actions, and custom regex for
`versions.env` / related pins). The config MUST be suitable as the shared source of truth for sync (#13): unused
managers or regexes MUST be harmless when matching files are absent. Product-specific overlays MAY be added later via
`extends` or thin local files; this change MUST land a complete Devinfra config seeded from the API Renovate config and
extended for Devinfra toolchain pins.

#### Scenario: Contributor opens renovate.json

- **WHEN** a contributor opens root `renovate.json` in Devinfra
- **THEN** they find enabled managers covering Docker, Dev Container, Python/uv (pep621), GitHub Actions, and
  `versions.env` regex pins
- **AND** the file is valid against the Renovate schema (or documented equivalent)

### Requirement: Per-repo Renovate GitHub workflow

The repository MUST provide `.github/workflows/renovate.yml` that runs self-hosted Renovate on a schedule, on
`workflow_dispatch`, and on push to the default branch when the Renovate config file changes. The workflow MUST use the
official Renovate GitHub Action (pinned) and MUST pass a repository Actions secret named `DEVINFRA_BOT_TOKEN` (not
`GITHUB_TOKEN` alone as the sole bot credential; the same secret is used by product-repo sync). The job MUST target the
current repository (not a multi-repo bot list in this change). The repository MUST NOT introduce `reusable-renovate.yml`
in this change.

#### Scenario: Maintainer opens the Renovate workflow

- **WHEN** a maintainer opens `.github/workflows/renovate.yml`
- **THEN** they find schedule, workflow_dispatch, and config-path push triggers
- **AND** the Renovate Action receives `secrets.DEVINFRA_BOT_TOKEN`
- **AND** there is no `reusable-renovate.yml` required to run Renovate in this repo

### Requirement: Renovate documentation covers token, dry-run, and Dependabot migration

The repository MUST document: (1) creating `DEVINFRA_BOT_TOKEN` as a GitHub Actions repository secret (fine-grained PAT
or equivalent scopes for contents/PRs as required by Renovate and product sync — not SOPS-in-repo); (2) local CLI
dry-run using the Dev Container pinned `renovate` against the shared config; (3) product migration — remove Dependabot
**version update** config (`dependabot.yml`); keep Dependabot **alerts**; prefer Renovate for dependency update PRs
(avoid dual general updaters); (4) sync/adoption via #13 for API / sql-to-arc / harvester. The root README Docs index
(or CI/Dev Container docs) MUST link to this documentation.

#### Scenario: Operator prepares Renovate on a new repo

- **WHEN** an operator follows the Renovate docs to enable automation
- **THEN** they learn to set repository secret `DEVINFRA_BOT_TOKEN` in GitHub Actions settings
- **AND** they find a local dry-run command using the pinned CLI
- **AND** they learn to remove Dependabot version updates while keeping alerts

### Requirement: Bot token is shared with product sync under one secret name

Renovate documentation and workflow MUST use the repository Actions secret `DEVINFRA_BOT_TOKEN` as the bot credential
(fine-grained PAT or GitHub App installation token material). The same secret MUST be the bot credential for
product-repo sync. Scopes MUST cover Contents and Pull requests on Devinfra and the three product targets (plus
Workflows/Issues as required by Renovate). Docs MUST NOT require SOPS-in-repo storage for that token and MUST NOT
document a second bot secret name (`RENOVATE_TOKEN`) as an alternate.

#### Scenario: Operator configures one bot for Renovate and sync

- **WHEN** an operator reads Renovate (and sync) token docs
- **THEN** they learn one secret `DEVINFRA_BOT_TOKEN` serves both workflows
- **AND** they learn required GitHub Actions secret setup (not SOPS)

### Requirement: Product Renovate skips Devinfra-synced dependency SoT

The shared `renovate.json` MUST disable dependency updates in the three product repositories
(`fairagro/m4.2_advanced_middleware_api`, `fairagro/m4.2_sql_to_arc`, `fairagro/m4.2_middleware_harvester`) for paths
and packages owned by Devinfra and delivered via sync (#13), including at least: `versions.env`, `.python-version`,
`docker/Dockerfile.product-app.base`, `.devcontainer/Dockerfile`, `renovate.json`, `.github/workflows/renovate.yml`,
`.github/workflows/codeql.yml`, and the BuildKit frontend package `docker/dockerfile`. Those updates MUST continue to
run in Devinfra. Product-local managers (e.g. pep621 under `middleware/`, product last-stage image tags other than the
disabled frontend package) MUST remain enabled in product repos.

#### Scenario: Product Renovate does not open versions.env CLI bump PRs

- **WHEN** Renovate runs in a product repo with the shared config
- **AND** newer GitHub-release CLI pins exist for entries in `versions.env`
- **THEN** it does not open a PR that only updates that synced `versions.env` file

#### Scenario: Product Renovate does not bump docker/dockerfile syntax tags

- **WHEN** Renovate runs in a product repo with the shared config
- **AND** a product Dockerfile contains `# syntax=docker/dockerfile:…`
- **THEN** it does not open a PR solely to bump that frontend package

#### Scenario: Product Renovate does not bump synced CodeQL workflow

- **WHEN** Renovate runs in a product repo with the shared config
- **AND** Action or related updates would only change `.github/workflows/codeql.yml`
- **THEN** it does not open a PR that only updates that synced CodeQL workflow
