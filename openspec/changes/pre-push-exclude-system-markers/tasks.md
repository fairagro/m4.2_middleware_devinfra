## 1. Pre-push hook

- [ ] 1.1 Update `.pre-commit-config.yaml` pre-push pytest `entry` to exclude `system_external` / `system_local` and
      print duration + `SKIP=pytest` banner
- [ ] 1.2 Confirm reusable CI pytest invocation does not inherit that `-m` filter

## 2. Docs

- [ ] 2.1 Document pre-push vs CI vs manual `system_*` in `docs/quality.md` (link #123 as deferred SoT)
- [ ] 2.2 Brief cross-link from `docs/ci.md` if CI pytest section exists

## 3. Specs

- [ ] 3.1 Apply delta to `openspec/specs/shared-quality-tooling/spec.md`
- [ ] 3.2 `openspec validate pre-push-exclude-system-markers --strict` and format/lint Markdown
