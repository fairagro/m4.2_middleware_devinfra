# Design: IDE mypy/pylint parity

## Context

See `proposal.md` (Why). Ruff already pins binary + `ruff.toml` in synced `.vscode/settings.json`. Mypy/pylint
extensions are installed but have no workspace settings. Path overlays already belong on process env / CI (`MYPYPATH`,
`pylint_source_roots`); Compose `product.env` can inject `MYPYPATH` into the Dev Container.

## Goals / Non-Goals

**Goals:**

- Same fragment files and `.venv` for IDE mypy/pylint as for hooks/CI
- Docs that cannot be read as “IDE may disagree” for those tools
- Keep overlays out of synced hook YAML and settings

**Non-Goals:**

- Bandit IDE extension
- Forwarding `PYLINT_SOURCE_ROOTS` through the synced pre-commit entry (A2)
- Making IDE whole-tree analysis match hook file sets (open-file vs `middleware/` is allowed)

## Decisions

1. **Settings live next to Ruff in `.vscode/settings.json`**, not in `devcontainer.json`
   `customizations.vscode.settings`. Alternative considered: Dev Container-only settings — rejected; host/Cursor windows
   would still miss them after sync.

2. **Minimal extension keys:** interpreter + `importStrategy: fromEnvironment` + `--config-file mypy.ini` /
   `--rcfile .pylintrc` + workspace cwd. No rule selects. Alternative: `mypy-type-checker.path` to the venv binary —
   interpreter + fromEnvironment matches the Ruff pattern and inherits `MYPYPATH`.

3. **Pylint `--source-roots` stays CI/env-only.** Document why hooks omit it (`fail-under`, no product paths in synced
   YAML). Alternative A2 (env-forwarding hook) deferred.

4. **Leave extension IDs installed.** Alternative B (uninstall) rejected at lock-in.

## Risks / Trade-offs

- [IDE open-file vs hook whole-tree] → Document: same config, same finding on the same file; hooks remain the commit
  gate.
- [Host checkout without `product.env` `MYPYPATH`] → Same as hooks on that host; Dev Container remains the supported
  environment.
- [Extension setting schema drift] → Pin keys used by current `ms-python.mypy-type-checker` / `ms-python.pylint`; fail
  closed to config-file path + interpreter only.

## Migration Plan

Sync settings + docs to products. No rollback beyond reverting the settings keys. Contributors may need to reload the
window once so the extensions pick up config paths.
