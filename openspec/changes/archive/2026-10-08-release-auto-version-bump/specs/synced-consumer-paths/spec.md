## ADDED Requirements

### Requirement: Sync allowlists Conventional Commits release helpers

`docs/synced-paths.yaml` MUST allowlist the fleet files products need for `version_bump: auto` and Conventional Commits
hygiene, including at least: shared `cliff.toml` (or equivalent git-cliff config), the version-detect helper script
under `scripts/`, commitlint config used by the shared pre-commit hook, and any new synced IDE/Copilot commit-message
instruction fragments introduced for this change (if not already covered by existing `.vscode/` /
`.github/copilot-instructions.md` allow entries).

#### Scenario: Product sync receives cliff and commitlint config

- **WHEN** a maintainer inspects `docs/synced-paths.yaml` after this change
- **THEN** they find allow entries for the shared git-cliff config and commitlint config (and detect script)
- **AND** products receive those paths on the next sync without hand-copy
