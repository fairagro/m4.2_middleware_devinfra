# Spec Delta

## MODIFIED Requirements

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
- **AND** Renovate artifacts and `versions.env` MAY be copied when listed on `foundation`
- **AND** python-product-only paths (e.g. `.devcontainer/**`, `.pre-commit-config.yaml`, `.python-version`) are not
  copied

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
token setup (shared with Renovate when applicable), the **operator checklist** to extend `DEVINFRA_BOT_TOKEN` access to
`fairagro/m4.2_infrastructure` and set the Infra repository secret before enabling live Infra sync, **profile-based**
allowlist ownership (`foundation` vs `python-product` vs `gitops` vs Infra-only profiles when present), hard excludes,
**delta orphan deletion** (per-target), **`SYNC-FOLLOWUP` trailer (body and comments)**, and the dispatch follow-up
input. Docs MUST state non-goals for Infra sync (foundation + gitops + Infra-only profiles as wired): no full
python-product allowlist, no verbatim product `.devcontainer/*`, no python-product pre-commit root, no
`.python-version`, and **Infra keeps owning its fat GitOps Dev Container until a dedicated adoption issue**. Docs MUST
state that Infra **does** receive Renovate artifacts and `versions.env` via foundation, and that unused pins do not
install tools by themselves. Docs MUST publish the Dev Container pin-ownership buckets (shared / python-product /
Infra-owned) or point to the Dev Container docs that do. Docs MUST NOT use obsolete lettered “wave” adopt labels for
sync coverage. The root README Docs index (or CI docs) MUST link to this documentation and MUST NOT describe sync paths
with those labels. Docs MUST note that push sync MAY keep `skip_infrastructure` default true until operators complete
the bot checklist.

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
- **AND** they learn Infra receives Renovate + `versions.env` via foundation after Slice 2
- **AND** they find the bot-access checklist before enabling live Infra sync
