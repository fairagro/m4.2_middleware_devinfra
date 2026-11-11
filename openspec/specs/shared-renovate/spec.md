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

### Requirement: Shared Renovate opens vulnerability fix PRs

The shared `renovate.json` MUST enable Renovate `vulnerabilityAlerts` so that, when GitHub Dependabot vulnerability
alerts are present and a fix version is available for a managed dependency, Renovate opens a remediation pull request.
It MUST enable `osvVulnerabilityAlerts` so Renovate also opens remediation pull requests for known OSV vulnerabilities
on **direct** dependencies using Renovate-supported datasources (at least those Renovate documents for OSV, including
`npm` and `pypi`). Vulnerability remediation PRs MUST carry a `security` label (in addition to the shared default
dependency labels when applicable) and MUST use a schedule of `at any time` so they are not deferred to maintenance
windows. Existing repository PR rate limits (`prHourlyLimit` / `prConcurrentLimit`) MAY still apply. This requirement
MUST NOT claim that Renovate consumes GitHub Code Scanning alerts (including Trivy SARIF).

#### Scenario: Dependabot alert can become a Renovate PR

- **WHEN** a repository using the shared config has an open Dependabot vulnerability alert for a Renovate-managed
  dependency with an available fix version
- **AND** Renovate runs successfully with a token that can read vulnerability alerts
- **THEN** Renovate opens (or updates) a remediation pull request for that dependency
- **AND** the PR is labeled `security`

#### Scenario: OSV direct-dependency vulnerability can become a Renovate PR

- **WHEN** a direct dependency managed by a supported OSV datasource has a known vulnerability with an available fix
- **AND** Renovate runs successfully
- **THEN** Renovate opens (or updates) a remediation pull request
- **AND** the PR is labeled `security`

#### Scenario: Code Scanning / Trivy stays out of Renovate vulnerability alerts

- **WHEN** a maintainer reads the shared Renovate vulnerability configuration or docs after this change
- **THEN** they learn vulnerability fix PRs come from Dependabot alerts and/or OSV
- **AND** they learn Trivy Code Scanning findings are not inputs to these Renovate knobs

### Requirement: Per-repo Renovate GitHub workflow

The repository MUST provide `.github/workflows/renovate.yml` that runs self-hosted Renovate on a schedule, on
`workflow_dispatch`, and on push to the default branch when the Renovate config file changes. The workflow MUST use the
official Renovate GitHub Action (pinned) and MUST pass a repository Actions secret named `DEVINFRA_BOT_TOKEN` (not
`GITHUB_TOKEN` alone as the sole bot credential; the same secret is used by product-repo sync). The job MUST target the
current repository (not a multi-repo bot list in this change). The repository MUST NOT introduce `reusable-renovate.yml`
in this change. The workflow MUST NOT pass `configurationFile: renovate.json` (or any repository config filename) to the
Action: that path becomes global `RENOVATE_CONFIG_FILE` and merges with the cloned repo’s `renovate.json`, duplicating
mergeable `customManagers` and causing `Cannot find replaceString` / branch update failures.

#### Scenario: Maintainer opens the Renovate workflow

- **WHEN** a maintainer opens `.github/workflows/renovate.yml`
- **THEN** they find schedule, workflow_dispatch, and config-path push triggers
- **AND** the Renovate Action receives `secrets.DEVINFRA_BOT_TOKEN`
- **AND** the Action does not set `configurationFile` to a repository Renovate config filename
- **AND** there is no `reusable-renovate.yml` required to run Renovate in this repo

### Requirement: Renovate documentation covers token, dry-run, and Dependabot migration

The repository MUST document: (1) creating `DEVINFRA_BOT_TOKEN` as a GitHub Actions repository secret (fine-grained PAT
or equivalent scopes for contents/PRs as required by Renovate and product sync — not SOPS-in-repo), including that the
token MUST be able to read GitHub Dependabot vulnerability alerts when `vulnerabilityAlerts` is enabled; (2) local CLI
dry-run using the Dev Container pinned `renovate` against the shared config; (3) product and Infra migration — remove
Dependabot **version update** config (`dependabot.yml`) after Renovate is green; keep Dependabot **alerts**; prefer
Renovate for dependency update PRs (avoid dual general updaters); turn off Dependabot **security update** PRs when
Renovate owns vulnerability remediation so only one bot opens fix PRs; (4) sync/adoption via #13 for API / sql-to-arc /
harvester **and** `m4.2_infrastructure` (foundation Renovate + `versions.env`); (5) that shared Renovate enables
`vulnerabilityAlerts` and `osvVulnerabilityAlerts`, with OSV limited to direct dependencies on supported datasources,
and that neither knob consumes Trivy / Code Scanning SARIF; (6) the operator **checklist** to grant the bot PAT access
to Infra, set `DEVINFRA_BOT_TOKEN` on Infra, run Infra sync dry-run then enable live sync, and note Infra#80; (7) an
Infra Dependabot wind-down **plan** (docs only in Devinfra — Infra deletes its version-update config locally after
Renovate is green). The root README Docs index (or CI/Dev Container docs) MUST link to this documentation.

#### Scenario: Operator prepares Renovate on a new repo

- **WHEN** an operator follows the Renovate docs to enable automation
- **THEN** they learn to set repository secret `DEVINFRA_BOT_TOKEN` in GitHub Actions settings
- **AND** they find a local dry-run command using the pinned CLI
- **AND** they learn to remove Dependabot version updates while keeping alerts
- **AND** they learn to prefer Renovate over Dependabot security-update PRs for vulnerability fixes
- **AND** they learn vulnerability fix PRs use Dependabot alerts and OSV, not Trivy Code Scanning

#### Scenario: Operator adopts Renovate on Infra

- **WHEN** an operator follows the Infra Slice-2 checklist in Renovate or sync docs
- **THEN** they learn to extend PAT access to `fairagro/m4.2_infrastructure` and set the Infra secret
- **AND** they learn to dry-run then enable Infra sync for Renovate + `versions.env`
- **AND** they find the Dependabot wind-down plan for Infra after Renovate is green

### Requirement: Bot token is shared with product sync under one secret name

Renovate documentation and workflow MUST use the repository Actions secret `DEVINFRA_BOT_TOKEN` as the bot credential
(fine-grained PAT or GitHub App installation token material). The same secret MUST be the bot credential for
product-repo sync. Scopes MUST cover Contents and Pull requests on Devinfra, the three product targets, and
`fairagro/m4.2_infrastructure` when Infra Renovate/sync is enabled (plus Workflows/Issues as required by Renovate). Docs
MUST NOT require SOPS-in-repo storage for that token and MUST NOT document a second bot secret name (`RENOVATE_TOKEN`)
as an alternate.

#### Scenario: Operator configures one bot for Renovate and sync

- **WHEN** an operator reads Renovate (and sync) token docs
- **THEN** they learn one secret `DEVINFRA_BOT_TOKEN` serves both workflows
- **AND** they learn required GitHub Actions secret setup (not SOPS)
- **AND** they learn Infra is on the repository-access list when Slice 2 is adopted

### Requirement: Product Renovate skips Devinfra-synced dependency SoT

The shared `renovate.json` MUST disable dependency updates in the three product repositories
(`fairagro/m4.2_advanced_middleware_api`, `fairagro/m4.2_sql_to_arc`, `fairagro/m4.2_middleware_harvester`) and in
`fairagro/m4.2_infrastructure` for paths and packages owned by Devinfra and delivered via sync (#13). For products that
includes at least: `versions.env`, `.python-version`, `docker/Dockerfile.product-app.base`, `.devcontainer/Dockerfile`,
`renovate.json`, `.github/workflows/renovate.yml`, `.github/workflows/codeql.yml`, and the BuildKit frontend package
`docker/dockerfile`. For Infra that includes at least: `versions.env`, `renovate.json`, and
`.github/workflows/renovate.yml`. Those updates MUST continue to run in Devinfra. Consumer-local managers (e.g. product
pep621 under `middleware/`, Infra-local Dockerfiles / workflows not on the skip list) MUST remain enabled in those
repos.

#### Scenario: Product Renovate does not open versions.env CLI bump PRs

- **WHEN** Renovate runs in a product repo with the shared config
- **AND** newer GitHub-release CLI pins exist for entries in `versions.env`
- **THEN** it does not open a PR that only updates that synced `versions.env` file

#### Scenario: Infra Renovate does not bump synced versions.env

- **WHEN** Renovate runs in `m4.2_infrastructure` with the shared config
- **AND** newer pins exist for entries in `versions.env`
- **THEN** it does not open a PR that only updates that synced pin file

#### Scenario: Product Renovate does not bump docker/dockerfile syntax tags

- **WHEN** Renovate runs in a product repo with the shared config
- **AND** a product Dockerfile contains `# syntax=docker/dockerfile:…`
- **THEN** it does not open a PR solely to bump that frontend package

#### Scenario: Product Renovate does not bump synced CodeQL workflow

- **WHEN** Renovate runs in a product repo with the shared config
- **AND** Action or related updates would only change `.github/workflows/codeql.yml`
- **THEN** it does not open a PR that only updates that synced CodeQL workflow
