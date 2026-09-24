# product-repo-sync Delta

## MODIFIED Requirements

### Requirement: Sync workflow opens PRs in the three product repos

The repository MUST provide a GitHub Actions workflow that can open sync pull requests in
`fairagro/m4.2_advanced_middleware_api`, `fairagro/m4.2_sql_to_arc`, and `fairagro/m4.2_middleware_harvester`. On push
to the default branch (`main`), when the run is not skipped, the workflow MUST attempt live sync PRs for those targets
(issue #13 done-when). The workflow MUST also support `workflow_dispatch` with inputs to dry-run (no PR) and/or skip
individual targets. Sync MUST authenticate with a repository Actions secret holding a bot token that has Contents and
Pull requests access on the target repos (same bot identity MAY be shared with Renovate). Each live sync that has
allowlisted changes MUST open a **new** sync PR per target (SHA-scoped branch); it MUST NOT force-update a single
rolling sync branch or reuse one open PR across runs (see also: one PR per run and supersede).

#### Scenario: Push to main can open sync PRs

- **WHEN** a commit lands on Devinfra `main` and sync is not skipped
- **THEN** the sync workflow runs and can open a **new** sync PR in each configured product repo when allowlisted paths
  differ
- **AND** the job uses the documented bot token secret (not `GITHUB_TOKEN` alone for cross-repo PRs)
- **AND** the job does not force-push an existing rolling sync branch to update a prior open PR

#### Scenario: Maintainer dry-runs or skips a consumer

- **WHEN** a maintainer runs `workflow_dispatch` with dry-run enabled or a target skip flag
- **THEN** the job reports what would sync without opening PRs (dry-run), or omits the skipped target
- **AND** documentation describes these overrides

## ADDED Requirements

### Requirement: Sync opens one PR per run and supersedes older open sync PRs

Because each sync copies the full allowlist snapshot, a later sync fully replaces an earlier open sync for the same
product. On a successful live sync that creates a new sync PR for a target, the implementation MUST use a branch name
that includes the Devinfra source short SHA (prefix `chore/devinfra-sync-`). It MUST then identify other **open** sync
PRs in that product repo whose head branch matches that sync prefix (including the legacy fixed branch
`chore/devinfra-sync` when still open), comment that each is superseded by the new PR number, and **close** those PRs
without merging. Sync MUST NOT auto-merge sync PRs as part of this behavior. Dry-run MUST NOT open, close, or comment on
PRs.

#### Scenario: New sync PR supersedes older open sync PRs

- **WHEN** live sync creates a new sync PR for a product repo and another sync PR is still open for that repo (legacy
  rolling branch or prior SHA-scoped sync branch)
- **THEN** the implementation comments on the older PR that it is superseded by the new PR
- **AND** closes the older PR without merging
- **AND** leaves the new PR open for human review/merge

#### Scenario: Dry-run does not supersede

- **WHEN** sync runs in dry-run mode
- **THEN** no sync PR is opened, closed, or commented for supersede
