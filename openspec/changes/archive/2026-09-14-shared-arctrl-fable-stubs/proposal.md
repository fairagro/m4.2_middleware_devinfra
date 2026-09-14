## Why

`arctrl` / `fable_library` ship without `py.typed`. Products either patch synced `mypy.ini` or litter
`# type: ignore[import-untyped]` on every import — both fight the Wave B sync contract. Harvester already proved a
shared incomplete stub tree + `MYPYPATH` / `stubPath` works; that tree belongs in Devinfra for all middleware products
([#67](https://github.com/fairagro/m4.2_middleware_devinfra/issues/67), comments: include `fable_library`).

## What Changes

- Add synced `stubs/arctrl/**` and `stubs/fable_library/**` (harvester seed: `__getattr__ -> Any` incomplete stubs) plus
  `stubs/README.md` documenting fleet vs product-local vs one-off silence.
- Allowlist those paths in `docs/synced-paths.yaml` (+ sync inventory).
- Document in `docs/quality.md`: put `stubs` on `MYPYPATH`; use `pyrightconfig.json` `stubPath` (#64); do **not** add
  `[mypy-arctrl*]` / fable overrides to synced `mypy.ini`; drop import-untyped ignores once stubs sync.
- Update `.agents/skills/arctrl/SKILL.md` to point at shared stubs instead of pyproject overrides / per-import ignores
  for arctrl and fable_library.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `shared-python-quality-config`: shared incomplete stubs for arctrl + fable_library; adoption docs (MYPYPATH /
  stubPath; no mypy.ini module overrides for those packages).
- `shared-arctrl-skill`: skill MUST NOT recommend import-untyped / mypy overrides for arctrl/fable when shared stubs are
  the fleet contract; MUST point agents at `stubs/`.

## Impact

- New allowlisted stub trees; quality/sync docs; arctrl skill examples; OpenSpec main sync on archive.
- Products: after sync, remove arctrl/fable ignores and keep owslib/rdflib stubs product-local (out of this PR).
