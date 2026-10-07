## 1. Feature-PR reusable

- [x] 1.1 Add optional `values_file` input (default empty) to `.github/workflows/reusable-helm-lint.yml` — verify the
      `workflow_call` inputs block lists it
- [x] 1.2 When `values_file` is non-empty and not skipped: assert the file exists; pass `-f` to `helm lint` and
      `helm template` — verify empty path keeps bare invocations

## 2. Local runner parity

- [x] 2.1 Update `scripts/run-helm-lint.sh` to honor `HELM_VALUES_FILE` (empty → bare; set → require file + `-f` on lint
      and template) — verify no-op without charts; fail closed on missing overlay file with a temp chart
- [x] 2.2 Document `HELM_VALUES_FILE` ↔ `values_file` parity in `docs/quality.md` and `docs/ci.md` — verify Prettier /
      markdownlint on touched docs

## 3. Validate

- [x] 3.1 Ensure both delta specs match the shipped workflow/runner/docs — verify
      `openspec validate helm-lint-values-file --strict`
