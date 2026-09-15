## ADDED Requirements

### Requirement: Workspace extensions recommendations are allowlisted

`docs/synced-paths.yaml` MUST list `.vscode/extensions.json` under `allow` so products receive the same VS Code / Cursor
extension recommendations as Devinfra after sync. The recommendations set MUST stay aligned with the shared Dev
Container extension list (see `shared-devcontainer-base`).

#### Scenario: extensions.json on allowlist

- **WHEN** a contributor inspects the product sync path allowlist
- **THEN** `.vscode/extensions.json` appears under `allow`
- **AND** it is not listed as a standing sync exclude
