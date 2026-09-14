## 1. Stub trees + allowlist

- [x] 1.1 Add `stubs/arctrl/**` and `stubs/fable_library/**` from harvester seed
- [x] 1.2 Add `stubs/README.md` (fleet vs product-local vs one-off)
- [x] 1.3 Allowlist `stubs/arctrl/**`, `stubs/fable_library/**`, `stubs/README.md` in `docs/synced-paths.yaml` (+
      sync.md inventory)

## 2. Docs + skill

- [x] 2.1 Update `docs/quality.md` for shared stubs / MYPYPATH / no mypy.ini arctrl overrides
- [x] 2.2 Update `.agents/skills/arctrl/SKILL.md` Package & Imports (+ example ignores) to prefer shared stubs
- [x] 2.3 Format/lint touched Markdown / skill

## 3. Validate

- [x] 3.1 `openspec validate shared-arctrl-fable-stubs --strict`
