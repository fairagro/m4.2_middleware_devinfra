## Why

Synced pre-push runs unfiltered `uv run pytest`, so product suites marked `system_external` / `system_local` (e.g. API
Testcontainers) make every `git push` feel hung. Product repos have registered those markers; Devinfra can now set a
fleet default exclude in the synced `.pre-commit-config.yaml`. Longer-term marker/coverage SoT without copying into
every `pyproject.toml` is deferred to [#123](https://github.com/fairagro/m4.2_middleware_devinfra/issues/123).

## What Changes

- Synced pre-push pytest entry: `uv run pytest -m "not system_external and not system_local"`, with a short banner that
  the stage may take minutes and that `SKIP=pytest` is an escape hatch (not the normal workflow).
- Docs (`docs/quality.md`, brief CI note if needed): pre-push = fast gate excluding `system_*`; CI / intentional local =
  broader suite; point at #123 for shared marker plugin / coverage fragment work.
- Do **not** implement the pytest-plugin / coverage-merge design from #123 in this change.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `shared-quality-tooling`: pre-push pytest MUST exclude `system_external` and `system_local` by default; MUST print
  duration / `SKIP=pytest` UX; docs MUST describe pre-push vs CI vs manual `system_*`.

## Impact

- Synced `.pre-commit-config.yaml` (and docs) in all product consumers after sync.
- CI reusable workflows stay on the broader suite (no silent inherit of the pre-push `-m` filter).
- Related: [#120](https://github.com/fairagro/m4.2_middleware_devinfra/issues/120), deferred
  [#123](https://github.com/fairagro/m4.2_middleware_devinfra/issues/123); product marker prep
  [API#416](https://github.com/fairagro/m4.2_advanced_middleware_api/issues/416),
  [harvester#222](https://github.com/fairagro/m4.2_middleware_harvester/issues/222),
  [sql-to-arc#141](https://github.com/fairagro/m4.2_sql_to_arc/issues/141).
