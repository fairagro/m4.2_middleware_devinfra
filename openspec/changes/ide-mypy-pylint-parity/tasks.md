# Tasks

## 1. IDE settings

- [ ] 1.1 Add mypy-type-checker and pylint keys to `.vscode/settings.json` (`.venv` interpreter,
      `importStrategy: fromEnvironment`, `--config-file mypy.ini` / `--rcfile .pylintrc`, workspace cwd); verify they
      are absent from `devcontainer.json` `customizations.vscode.settings`
- [ ] 1.2 Confirm extensions.json / Dev Container still recommend `ms-python.mypy-type-checker` and `ms-python.pylint`
      (no uninstall)

## 2. Docs

- [ ] 2.1 Update `docs/quality.md` parity table and IDE section: mypy/pylint are IDE surfaces using the fragments;
      Bandit stays hooks+CI only; open-file vs hook tree is allowed; verify no remaining “hooks + CI only” for mypy or
      pylint
- [ ] 2.2 Document pylint `--source-roots` as CI/`pylint_source_roots` + product.env overlay (hooks omit it; not the
      fail bar); verify `docs/quality.md` and/or `mypy.ini` / `.pylintrc` headers still forbid synced YAML patches

## 3. Validate

- [ ] 3.1 Run `openspec validate ide-mypy-pylint-parity --strict` and confirm pass
