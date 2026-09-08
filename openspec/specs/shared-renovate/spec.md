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
official Renovate GitHub Action (pinned) and MUST pass a repository Actions secret named `RENOVATE_TOKEN` (not
`GITHUB_TOKEN` alone as the sole bot credential). The job MUST target the current repository (not a multi-repo bot list
in this change). The repository MUST NOT introduce `reusable-renovate.yml` in this change.

#### Scenario: Maintainer opens the Renovate workflow

- **WHEN** a maintainer opens `.github/workflows/renovate.yml`
- **THEN** they find schedule, workflow_dispatch, and config-path push triggers
- **AND** the Renovate Action receives `secrets.RENOVATE_TOKEN`
- **AND** there is no `reusable-renovate.yml` required to run Renovate in this repo

### Requirement: Renovate documentation covers token, dry-run, and Dependabot migration

The repository MUST document: (1) creating `RENOVATE_TOKEN` as a GitHub Actions repository secret (fine-grained PAT or
equivalent scopes for contents/PRs as required by Renovate — not SOPS-in-repo); (2) local CLI dry-run using the Dev
Container pinned `renovate` against the shared config; (3) product migration — remove Dependabot **version update**
config (`dependabot.yml`); keep Dependabot **alerts**; prefer Renovate for dependency update PRs (avoid dual general
updaters); (4) sync/adoption via #13 for API / sql-to-arc / harvester. The root README Docs index (or CI/Dev Container
docs) MUST link to this documentation.

#### Scenario: Operator prepares Renovate on a new repo

- **WHEN** an operator follows the Renovate docs to enable automation
- **THEN** they learn to set repository secret `RENOVATE_TOKEN` in GitHub Actions settings
- **AND** they find a local dry-run command using the pinned CLI
- **AND** they learn to remove Dependabot version updates while keeping alerts
