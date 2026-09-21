## Why

Fleet marker vocabulary is still hand-copied into each product `pyproject.toml` because pytest does not merge configs
the way Ruff/Mypy fragments do. A shared plugin/coverage pattern is the right SoT, but shipping it now is expensive
relative to the working copy-paste path (#120/#121). This change **locks the design contract only** so a later
implementation PR has an agreed adopt path—without claiming the capability exists yet.

## What Changes

- Record the locked design: **pytest plugin for fleet markers first**; **coverage fragment deferred** as a linked
  follow-up
- Document adopt expectations (what stays in product `pyproject.toml`, how the plugin is loaded, non-goals)
- Update synced `docs/quality.md` deferred section so the SoT pointer matches this design (not implement the plugin)
- **No** plugin package, **no** `.coveragerc` ship, **no** `synced-paths.yaml` allowlist entry for unimplemented paths
- **No** main-spec requirement sync in this change (`skip_specs: true` — behavior unchanged until an implement change)

## Capabilities

### New Capabilities

- (none in this change — design/docs only; `skip_specs: true`)

### Modified Capabilities

- (none — a future implement change will extend `shared-python-quality-config` and/or `shared-quality-tooling` with real
  delta specs)

## Impact

- OpenSpec change artifacts under `openspec/changes/fleet-pytest-markers-plugin-design/`
- `docs/quality.md` (deferred / planned-SoT wording only)
- Products: no adopt required until a follow-up implement PR
- Issue [#123](https://github.com/fairagro/m4.2_middleware_devinfra/issues/123)
