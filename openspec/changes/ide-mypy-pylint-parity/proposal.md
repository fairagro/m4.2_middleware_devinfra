# IDE mypy/pylint parity

## Why

Fleet docs require IDE / hooks / CI to share the same quality findings, but synced settings leave the installed mypy and
pylint extensions unconfigured. Contributors trust a clean Problems panel, then hit hook/CI failures (e.g. mypy
`no-any-return`). The extensions should use the same fragments as hooks and CI, not a second rule set.

## What Changes

- Wire synced `.vscode/settings.json` so `ms-python.mypy-type-checker` and `ms-python.pylint` use the project `.venv`
  and `mypy.ini` / `.pylintrc` (Ruff-shaped: config path + interpreter, no restated policy flags).
- Keep installing those extensions. Path overlays stay env/CI (`MYPYPATH`, reusable `pylint_source_roots`) — not product
  paths in synced settings or `.pre-commit-config.yaml`.
- Document that pre-commit pylint still omits `--source-roots` because product paths cannot live in the synced hook
  YAML; E0401 is not the fail bar (`fail-under`).
- Update `docs/quality.md` so mypy/pylint are IDE parity surfaces. Bandit stays the named hooks+CI-only exception.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `shared-quality-tooling`: three-environment parity MUST treat mypy/pylint as IDE surfaces; Bandit remains the
  documented IDE exception
- `shared-devcontainer-base`: synced workspace settings MUST point the mypy and pylint extensions at the shared
  fragments and `.venv`

## Impact

- `.vscode/settings.json`, `docs/quality.md` (parity table + IDE section)
- Optional comment/header notes on `mypy.ini` / `.pylintrc` / pre-commit pylint entry (no product paths in synced YAML)
- Product sync inherits settings after merge; `.devcontainer/product.env` remains the MYPYPATH overlay
