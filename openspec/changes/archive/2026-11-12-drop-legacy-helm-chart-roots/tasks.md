## 1. Runner and hooks

- [x] 1.1 Update `scripts/run-helm-lint.sh` to discover only `charts/*/Chart.yaml` — verify skip message and loop
- [x] 1.2 Narrow `.pre-commit-config.yaml` and `.pre-commit-config.infrastructure.yaml` helm-lint `files` and
      `check-yaml` excludes to `charts/` — verify no `helm|helmchart` in those entries

## 2. IDE and docs

- [x] 2.1 Drop legacy globs from `.vscode/settings.json` `files.associations` — verify only `charts/**/templates`
- [x] 2.2 Update `docs/quality.md`, `docs/ci.md`, and related dual-discovery prose — verify no “deprecated dual
      discovery” / migration window language remains for chart roots

## 3. Validate

- [x] 3.1 Run `openspec validate drop-legacy-helm-chart-roots --strict` and Prettier/markdownlint on touched Markdown —
      verify clean
