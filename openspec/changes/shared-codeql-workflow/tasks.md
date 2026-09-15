## 1. Workflow

- [ ] 1.1 Add `.github/workflows/codeql.yml` (T2a+weekly, matrix actions+python, P1 refs, I1 bootstrap)
- [ ] 1.2 Confirm workflow is not named `reusable-*.yml`

## 2. Sync + Renovate

- [ ] 2.1 Allowlist `.github/workflows/codeql.yml` in `docs/synced-paths.yaml`
- [ ] 2.2 Add path to product `matchFileNames` disable in `renovate.json`
- [ ] 2.3 Update `docs/renovate.md` disable table and `docs/ci.md` CodeQL note

## 3. Specs

- [ ] 3.1 Apply deltas: `shared-codeql` (new), `synced-consumer-paths`, `shared-renovate`
- [ ] 3.2 `openspec validate shared-codeql-workflow --strict` and format/lint Markdown
