## MODIFIED Requirements

### Requirement: Sync documentation is indexed

The repository MUST document sync purpose, triggers (main push + dispatch), dry-run/skip (including infrastructure), bot
token setup (shared with Renovate when applicable; Infra token access called out as a later slice when needed),
**profile-based** allowlist ownership (`foundation` vs `python-product` vs `gitops` when present), hard excludes,
**delta orphan deletion** (per-target), **`SYNC-FOLLOWUP` trailer (body and comments)**, and the dispatch follow-up
input. Docs MUST state non-goals for foundation-only / foundation+gitops Infra sync: no full python-product allowlist,
no verbatim product `.devcontainer/*`, no python-product pre-commit fragment or composed product hook blob, no
Renovate/`versions.env` until that slice. Docs MUST NOT use obsolete “Wave A” / “Wave-A” terminology for sync coverage.
The root README Docs index (or CI docs) MUST link to this documentation and MUST NOT describe sync paths as “Wave A”.

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
