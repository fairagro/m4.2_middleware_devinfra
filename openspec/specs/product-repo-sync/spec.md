# product-repo-sync Specification

## Purpose

Defines automation that opens pull requests in the three m4.2 product repositories copying only Devinfra paths listed in
the single synced-paths allowlist, so a commit on Devinfra main can propagate shared files without hand-copy Wave
adopts.

## Requirements

### Requirement: Sync workflow opens PRs in the three product repos

The repository MUST provide a GitHub Actions workflow that can open sync pull requests in
`fairagro/m4.2_advanced_middleware_api`, `fairagro/m4.2_sql_to_arc`, and `fairagro/m4.2_middleware_harvester`, and MUST
also support an optional fourth target `infrastructure` → `fairagro/m4.2_infrastructure`. On push to the default branch
(`main`), when the run is not skipped, the workflow MUST attempt live sync PRs for the configured python-product targets
(issue #13 done-when). The `infrastructure` target MAY default to skipped on push until operators enable it (bot access
/ adoption); dry-run and dispatch MUST still be able to include it. The workflow MUST also support `workflow_dispatch`
with inputs to dry-run (no PR) and/or skip individual targets (including `skip_infrastructure`). Sync MUST authenticate
with a repository Actions secret holding a bot token that has Contents and Pull requests access on the target repos
being synced (same bot identity MAY be shared with Renovate). The bot token MUST also be able to create issues on those
target repos when follow-up creation runs. Each live sync that has allowlisted changes MUST open a **new** sync PR per
target (SHA-scoped branch); it MUST NOT force-update a single rolling sync branch or reuse one open PR across runs (see
also: one PR per run and supersede).

On push-triggered live sync, the workflow MUST resolve the Devinfra pull request associated with source `HEAD` (when one
exists), collect `SYNC-FOLLOWUP: <stable-id>` trailers from that PR’s body and comments, and for each distinct id ensure
a deduplicated follow-up issue exists in each non-skipped **python-product** target (via the agent-ai-gh / `m42-ai`
plumbing). Follow-up ensure for `infrastructure` MAY be omitted while that target is foundation-only / not yet adopting
product follow-up trailers. `workflow_dispatch` MUST accept an optional follow-up id input that triggers the same
per-product ensure path without requiring a merged PR trailer.

#### Scenario: Push to main can open sync PRs

- **WHEN** a commit lands on Devinfra `main` and sync is not skipped
- **THEN** the sync workflow runs and can open a **new** sync PR in each non-skipped configured consumer when that
  target’s allowlisted paths differ **or** allowlist orphans must be deleted
- **AND** the job uses the documented bot token secret (not `GITHUB_TOKEN` alone for cross-repo PRs)
- **AND** the job does not force-push an existing rolling sync branch to update a prior open PR

#### Scenario: Maintainer dry-runs or skips a consumer

- **WHEN** a maintainer runs `workflow_dispatch` with dry-run enabled or a target skip flag (including infrastructure)
- **THEN** the job reports what would sync without opening PRs (dry-run), or omits the skipped target
- **AND** documentation describes these overrides

#### Scenario: Trailer opens product follow-up issues

- **WHEN** live push sync runs and the merged Devinfra PR for `HEAD` contains `SYNC-FOLLOWUP: <stable-id>` in its body
  or comments
- **THEN** each non-skipped python-product repo has an open follow-up issue for that id (create or reuse)
- **AND** a second sync with the same id does not open a duplicate open issue

#### Scenario: Dispatch follow-up input

- **WHEN** a maintainer runs `workflow_dispatch` with a follow-up id input set
- **THEN** each non-skipped python-product repo gets the same ensure-follow-up behavior as a trailer id
- **AND** dry-run MUST NOT create issues

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

### Requirement: Sync copies only the allowlist SoT paths

The sync implementation MUST resolve the set of paths to copy exclusively from `docs/synced-paths.yaml` (the sole path
SoT), using that file’s `profiles` and per-target `profiles` list (effective allow = union of those profile `allow`
lists). It MUST NOT maintain a second hand-edited path list. It MUST refuse to copy paths matching the YAML `exclude`
list (and MUST hard-exclude at least: product `middleware/` trees, `openspec/specs/**`, `openspec/changes/**`,
documented product-local overlays, and `.github/workflows/reusable-*.yml`). Only paths present in the target’s effective
allow (including globs expanded against this repo) MAY be written into that target’s PRs.

When a live sync (or non-dry-run dispatch) has a usable comparison base (workflow push `before` SHA, or an explicit base
SHA for local/testing), the implementation MUST compute the resolved allowlist file set **for that target** at that base
and at the source `HEAD` commit. Paths present in the base set and absent from the `HEAD` set are **allowlist orphans**
for that run and target. For each such path that still exists in the consumer checkout, the sync PR MUST remove it
(`git rm` or equivalent). The implementation MUST NOT require a `retire:` (or equivalent) list in
`docs/synced-paths.yaml`. Paths that were never in the resolved allowlist file set for that target MUST NOT be deleted
by this mechanism.

When no usable base SHA exists, the implementation MUST still copy the current allowlist set for the target and MUST NOT
invent deletes from heuristics unrelated to the allowlist delta.

#### Scenario: Allowlist is the only path input

- **WHEN** sync runs for a target
- **THEN** the paths copied are derived from `docs/synced-paths.yaml` profiles selected for that target
- **AND** no separate sync-manifest file is required as a second source of truth

#### Scenario: Infrastructure receives foundation only

- **WHEN** sync builds the file set for the `infrastructure` target
- **THEN** the effective allow is the union of that target’s profiles (foundation + gitops + Infra-only as wired) and
  MUST NOT include `python-product`
- **AND** python-product-only paths (e.g. `.devcontainer/**`, `.pre-commit-config.yaml`, Renovate, `versions.env`) are
  not copied

#### Scenario: OpenSpec specs and middleware are never synced

- **WHEN** sync builds the file set for a product PR
- **THEN** it does not include `openspec/specs/**` or `openspec/changes/**` from Devinfra
- **AND** it does not write into product `middleware/`
- **AND** it does not copy `reusable-*.yml` workflow files

#### Scenario: Allowlist orphan is removed in the sync PR

- **WHEN** a path is in the resolved allowlist file set for that target at the comparison base and not at source `HEAD`,
  and that path exists in the consumer checkout
- **THEN** the sync PR deletes that path in the consumer repo
- **AND** no `retire:` entry is required in `docs/synced-paths.yaml`

#### Scenario: Never-allowlisted product path is kept

- **WHEN** a product path was never in the resolved allowlist file set for that target for the comparison window
- **THEN** sync does not delete that path solely because a sibling allowlisted path was removed

#### Scenario: Sync does not delete in product repos

- **WHEN** sync runs without a usable comparison base SHA for the allowlist delta
- **THEN** the sync implementation does not remove consumer paths based on an allowlist delta
- **AND** it still copies the current allowlist set for the target

### Requirement: Sync documentation is indexed

The repository MUST document sync purpose, triggers (main push + dispatch), dry-run/skip (including infrastructure), bot
token setup (shared with Renovate when applicable; Infra token access called out as a later slice when needed),
**profile-based** allowlist ownership (`foundation` vs `python-product` vs `gitops` vs Infra-only profiles when
present), hard excludes, **delta orphan deletion** (per-target), **`SYNC-FOLLOWUP` trailer (body and comments)**, and
the dispatch follow-up input. Docs MUST state non-goals for Infra sync (foundation + gitops + Infra-only profiles as
wired): no full python-product allowlist, no verbatim product `.devcontainer/*`, no python-product pre-commit root, no
Renovate/`versions.env` until that slice, and **Infra keeps owning its fat GitOps Dev Container until a dedicated
adoption issue**. Docs MUST publish the Dev Container pin-ownership buckets (shared / python-product / Infra-owned) or
point to the Dev Container docs that do. Docs MUST NOT use obsolete lettered “wave” adopt labels for sync coverage. The
root README Docs index (or CI docs) MUST link to this documentation and MUST NOT describe sync paths with those labels.

#### Scenario: Contributor finds sync docs

- **WHEN** a contributor opens the README Docs section
- **THEN** they find a link to the sync documentation
- **AND** the docs name the python-product targets, the optional `infrastructure` target, and the allowlist file
  profiles

#### Scenario: Contributor learns delete and follow-up contract

- **WHEN** a contributor reads the sync documentation
- **THEN** they learn that allowlist orphans are removed via delta `git rm` without a `retire:` list (per target profile
  set)
- **AND** they learn how to set `SYNC-FOLLOWUP: <id>` on a Devinfra PR and via dispatch

#### Scenario: Contributor learns Infra Dev Container non-goals

- **WHEN** a contributor reads sync non-goals for the `infrastructure` target
- **THEN** they learn product `.devcontainer/*` is never synced to Infra by accident
- **AND** they learn Infra owns its GitOps Dev Container until an adoption issue
- **AND** they find or are pointed at pin-ownership buckets (shared vs python-product vs Infra-owned)
