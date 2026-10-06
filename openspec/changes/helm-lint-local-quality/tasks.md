## 1. Runner

- [ ] 1.1 Add `scripts/run-helm-lint.sh` that discovers `helmchart/*/Chart.yaml` and `helm/*/Chart.yaml`, no-ops when
      none, otherwise `helm lint` + `helm template ci-smoke` per chart — verify: no charts in this repo → exit 0; a temp
      chart dir → lint/template run (or fail closed without `helm`)
- [ ] 1.2 Make the script executable and fail with Dev Container / `HELM_VERSION` guidance when charts exist but `helm`
      is missing — verify by `PATH=` empty invocation against a fake chart (or documented dry run)

## 2. Pre-commit + docs

- [ ] 2.1 Add a commit-stage local hook in `.pre-commit-config.yaml` calling the runner (`files: ^(helm|helmchart)/`)
      and allowlist `scripts/run-helm-lint.sh` in `docs/synced-paths.yaml` — verify
      `uv run pre-commit run helm-lint --all-files` succeeds in this repo
- [ ] 2.2 Document local hook vs Feature-PR reusable in `docs/quality.md` (and a short pointer in `docs/ci.md`) — verify
      `npx prettier --check` / `npm run lint:md` on touched docs

## 3. Spec alignment

- [ ] 3.1 Ensure the delta spec matches the shipped runner/hook/docs — verify
      `openspec validate helm-lint-local-quality --strict`
