## MODIFIED Requirements

### Requirement: Sync workflow opens PRs in the three product repos

The repository MUST provide a GitHub Actions workflow that can open sync pull requests in
`fairagro/m4.2_advanced_middleware_api`, `fairagro/m4.2_sql_to_arc`, and `fairagro/m4.2_middleware_harvester`, and MUST
also support a fourth target `infrastructure` → `fairagro/m4.2_infrastructure`. On push to the default branch (`main`),
when the run is not skipped, the workflow MUST attempt live sync PRs for the configured python-product targets **and**
the `infrastructure` target (issue #13 / #388). The workflow MUST NOT hard-skip `infrastructure` on push. The workflow
MUST also support `workflow_dispatch` with inputs to dry-run (no PR) and/or skip individual targets (including
`skip_infrastructure`). The `skip_infrastructure` dispatch input MUST default to **false** so live/dry-run dispatch
includes Infra unless an operator explicitly skips it. Sync MUST authenticate with a repository Actions secret holding a
bot token that has Contents and Pull requests access on the target repos being synced (same bot identity MAY be shared
with Renovate). The bot token MUST also be able to create issues on those target repos when follow-up creation runs.
Each live sync that has allowlisted changes MUST open a **new** sync PR per target (SHA-scoped branch); it MUST NOT
force-update a single rolling sync branch or reuse one open PR across runs (see also: one PR per run and supersede).

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

#### Scenario: Push includes infrastructure by default

- **WHEN** a commit lands on Devinfra `main` and the allowlist gate says sync
- **THEN** the sync job does not pass `--skip-infrastructure` solely because the event is push
- **AND** `infrastructure` is synced unless a documented emergency override is used

#### Scenario: Maintainer dry-runs or skips a consumer

- **WHEN** a maintainer runs `workflow_dispatch` with dry-run enabled or a target skip flag (including infrastructure)
- **THEN** the job reports what would sync without opening PRs (dry-run), or omits the skipped target
- **AND** documentation describes these overrides
- **AND** `skip_infrastructure` defaults to false so Infra is included unless the maintainer sets it true

#### Scenario: Trailer opens product follow-up issues

- **WHEN** live push sync runs and the merged Devinfra PR for `HEAD` contains `SYNC-FOLLOWUP: <stable-id>` in its body
  or comments
- **THEN** each non-skipped python-product repo has an open follow-up issue for that id (create or reuse)
- **AND** a second sync with the same id does not open a duplicate open issue

#### Scenario: Dispatch follow-up input

- **WHEN** a maintainer runs `workflow_dispatch` with a follow-up id input set
- **THEN** each non-skipped python-product repo gets the same ensure-follow-up behavior as a trailer id
- **AND** dry-run MUST NOT create issues

### Requirement: Sync documentation is indexed

The repository MUST document sync purpose, triggers (main push + dispatch), dry-run/skip (including infrastructure), bot
token setup (shared with Renovate when applicable), the **completed** Slice-2 operator checklist for Infra Renovate +
sync (PAT + Infra secret), **profile-based** allowlist ownership (`foundation` vs `python-product` vs `gitops` vs
Infra-only profiles when present), hard excludes, **delta orphan deletion** (per-target), **`SYNC-FOLLOWUP` trailer
(body and comments)**, and the dispatch follow-up input. Docs MUST state non-goals for Infra sync (foundation + gitops +
Infra-only profiles as wired): no full python-product allowlist, no verbatim product `.devcontainer/*`, no
python-product pre-commit root, no `.python-version`, and **Infra keeps owning its fat GitOps Dev Container until a
dedicated adoption issue**. Docs MUST state that Infra **does** receive Renovate artifacts and `versions.env` via
foundation, and that unused pins do not install tools by themselves. Docs MUST publish the Dev Container pin-ownership
buckets (shared / python-product / Infra-owned) or point to the Dev Container docs that do. Docs MUST NOT use obsolete
lettered “wave” adopt labels for sync coverage. The root README Docs index (or CI docs) MUST link to this documentation
and MUST NOT describe sync paths with those labels. Docs MUST state that push and dispatch **include** `infrastructure`
by default after Slice-2, and MUST document how operators set `skip_infrastructure=true` on dispatch when they need to
omit Infra.

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

#### Scenario: Contributor learns Infra is included by default

- **WHEN** a contributor reads sync / Renovate Slice-2 docs after this change
- **THEN** they learn push and dispatch include `infrastructure` by default
- **AND** they learn how to set `skip_infrastructure=true` on dispatch when omitting Infra
