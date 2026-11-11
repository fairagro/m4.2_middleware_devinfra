## 1. Runner and hooks

- [ ] 1.1 Update `scripts/run-helm-lint.sh` to discover `charts/*/Chart.yaml` first, then deprecated
      `helmchart/*/Chart.yaml` and `helm/*/Chart.yaml`; adjust skip/error messages; verify by running the script in this
      repo (no charts → exit 0) and with a temporary `charts/fixture/Chart.yaml` smoke if practical
- [ ] 1.2 Update `.pre-commit-config.yaml` helm-lint `files` to `^(charts|helm|helmchart)/` and extend `check-yaml`
      exclude for `charts/**/templates`; verify config parses (`pre-commit validate-config` or equivalent) and comments
      mention canonical `charts/`

## 2. IDE and docs

- [ ] 2.1 Add `**/charts/**/templates/**` Helm `files.associations` in `.vscode/settings.json` (keep legacy globs);
      verify JSON validity and that associations include `charts`
- [ ] 2.2 Update `docs/quality.md` (and `docs/sync.md` helmchart example if needed) for canonical `charts/`, dual
      discovery deprecation, and no `helmcharts/` alias; verify with a quick grep that docs no longer present dual roots
      as equal SoT
- [ ] 2.3 Update `docs/ci.md` Feature-PR / Helm examples and path-filter guidance to `charts/`; verify examples use
      `charts/` not `helmchart/` as the recommended path

## 3. Validate

- [ ] 3.1 Run `openspec validate standardize-helm-charts-root --strict` and fix any delta issues; verify exit 0
- [ ] 3.2 Run Prettier/markdownlint on touched Markdown (`npm run format:md` / `lint:md` scoped or full as needed) and
      verify clean for changed paths
