# product-repo-sync Specification

## Purpose

Defines automation that opens pull requests in the three m4.2 product repositories copying only Devinfra paths listed in
the single synced-paths allowlist, so a commit on Devinfra main can propagate shared files without hand-copy Wave
adopts.

## Requirements

### Requirement: Sync workflow opens PRs in the three product repos

The repository MUST provide a GitHub Actions workflow that can open sync pull requests in
`fairagro/m4.2_advanced_middleware_api`, `fairagro/m4.2_sql_to_arc`, and `fairagro/m4.2_middleware_harvester`. On push
to the default branch (`main`), when the run is not skipped, the workflow MUST attempt live sync PRs for those targets
(issue #13 done-when). The workflow MUST also support `workflow_dispatch` with inputs to dry-run (no PR) and/or skip
individual targets. Sync MUST authenticate with a repository Actions secret holding a bot token that has Contents and
Pull requests access on the target repos (same bot identity MAY be shared with Renovate).

#### Scenario: Push to main can open sync PRs

- **WHEN** a commit lands on Devinfra `main` and sync is not skipped
- **THEN** the sync workflow runs and can open (or update) a sync PR in each configured product repo when allowlisted
  paths differ
- **AND** the job uses the documented bot token secret (not `GITHUB_TOKEN` alone for cross-repo PRs)

#### Scenario: Maintainer dry-runs or skips a consumer

- **WHEN** a maintainer runs `workflow_dispatch` with dry-run enabled or a target skip flag
- **THEN** the job reports what would sync without opening PRs (dry-run), or omits the skipped target
- **AND** documentation describes these overrides

### Requirement: Sync copies only the allowlist SoT paths

The sync implementation MUST resolve the set of paths to copy exclusively from `docs/synced-paths.yaml` (the sole path
SoT). It MUST NOT maintain a second hand-edited path list. It MUST refuse to copy paths matching the YAML `exclude` list
(and MUST hard-exclude at least: product `middleware/` trees, `openspec/specs/**`, `openspec/changes/**`, documented
product-local overlays, and `.github/workflows/reusable-*.yml`). Only paths present under `allow` (including globs
expanded against this repo) MAY be written into target PRs.

#### Scenario: Allowlist is the only path input

- **WHEN** sync runs
- **THEN** the paths copied are derived from `docs/synced-paths.yaml`
- **AND** no separate sync-manifest file is required as a second source of truth

#### Scenario: OpenSpec specs and middleware are never synced

- **WHEN** sync builds the file set for a product PR
- **THEN** it does not include `openspec/specs/**` or `openspec/changes/**` from Devinfra
- **AND** it does not write into product `middleware/`
- **AND** it does not copy `reusable-*.yml` workflow files

### Requirement: Sync documentation is indexed

The repository MUST document sync purpose, triggers (main push + dispatch), dry-run/skip, bot token setup (shared with
Renovate when applicable), allowlist ownership, and hard excludes. The root README Docs index (or CI docs) MUST link to
this documentation.

#### Scenario: Contributor finds sync docs

- **WHEN** a contributor opens the README Docs section
- **THEN** they find a link to the sync documentation
- **AND** the docs name the three product targets and the allowlist file
