## 1. Workflow

- [x] 1.1 Add `.github/workflows/codeql.yml` (T2a+weekly, matrix actions+python, P1 refs, I1 bootstrap)
- [x] 1.2 Confirm workflow is not named `reusable-*.yml`

## 2. Sync + Renovate

- [x] 2.1 Allowlist `.github/workflows/codeql.yml` in `docs/synced-paths.yaml`
- [x] 2.2 Add path to product `matchFileNames` disable in `renovate.json`
- [x] 2.3 Update `docs/renovate.md` disable table and `docs/ci.md` CodeQL note

## 3. Specs

- [x] 3.1 Apply deltas: `shared-codeql` (new), `synced-consumer-paths`, `shared-renovate`
- [x] 3.2 `openspec validate shared-codeql-workflow --strict` and format/lint Markdown
