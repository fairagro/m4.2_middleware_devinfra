## 1. Stub trees + allowlist

- [ ] 1.1 Add `stubs/arctrl/**` and `stubs/fable_library/**` from harvester seed
- [ ] 1.2 Add `stubs/README.md` (fleet vs product-local vs one-off)
- [ ] 1.3 Allowlist `stubs/arctrl/**`, `stubs/fable_library/**`, `stubs/README.md` in `docs/synced-paths.yaml` (+
      sync.md inventory)

## 2. Docs + skill

- [ ] 2.1 Update `docs/quality.md` for shared stubs / MYPYPATH / no mypy.ini arctrl overrides
- [ ] 2.2 Update `.agents/skills/arctrl/SKILL.md` Package & Imports (+ example ignores) to prefer shared stubs
- [ ] 2.3 Format/lint touched Markdown / skill

## 3. Validate

- [ ] 3.1 `openspec validate shared-arctrl-fable-stubs --strict`
