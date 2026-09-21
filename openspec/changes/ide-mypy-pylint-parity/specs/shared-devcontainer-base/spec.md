## ADDED Requirements

### Requirement: Synced IDE settings for mypy and pylint

Synced `.vscode/settings.json` MUST configure the recommended Mypy and Pylint extensions to use the workspace `.venv`
interpreter and the shared fragment files (`mypy.ini`, `.pylintrc`) as their only policy source. Settings MUST be
limited to interpreter / import strategy, config-file path (or equivalent pointing at those fragments), and cwd of the
workspace. They MUST NOT restate fragment-expressible policy (rule selects, line length, severity). They MUST NOT embed
product `middleware/` path overlays; `MYPYPATH` and pylint `--source-roots` remain process env / reusable CI inputs
(including optional `.devcontainer/product.env`). Those keys MUST live in `.vscode/settings.json` (not duplicated under
`devcontainer.json` `customizations.vscode.settings`).

#### Scenario: Mypy and pylint extensions use shared fragments

- **WHEN** a contributor inspects synced `.vscode/settings.json` with the mypy-type-checker and pylint extensions
  installed
- **THEN** both extensions are pointed at `${workspaceFolder}/.venv` and at `mypy.ini` / `.pylintrc`
- **AND** the settings do not list product package path overlays
- **AND** those keys are absent from `devcontainer.json` `customizations.vscode.settings`
