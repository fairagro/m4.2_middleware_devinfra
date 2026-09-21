## Context

See `proposal.md` — Why. Today products duplicate fleet pytest markers in local `pyproject.toml` so the synced
pre-push expression `-m "not system_external and not system_local"` stays valid under `--strict-markers`. Pytest does
not merge config files; a synced `pytest.ini` that only registers markers would displace product `testpaths` /
`pythonpath`. Coverage tables have the same first-wins problem. Related work (#120/#121) shipped the marker filter with
local registration; #123 deferred a real SoT.

This change documents the **future implement contract** only. Apply updates `docs/quality.md`; it does **not** add a
plugin or coverage fragment.

## Goals / Non-Goals

**Goals:**

- Lock a single preferred SoT for fleet markers (plugin) and an explicit deferral for coverage
- Define what remains product-owned vs what a later Devinfra implement PR must ship and sync
- Give products a clear adopt sketch so the implement PR is not a design debate

**Non-Goals:**

- Implementing the plugin, packaging, or sync allowlist entries in this change
- Shipping a coverage fragment in this change
- Syncing root `pyproject.toml`, forking `.pre-commit-config.yaml` marker lists, or moving product `testpaths` into
  Devinfra
- Updating main OpenSpec capability requirements until an implement change lands real deltas

## Decisions

1. **Markers SoT = pytest plugin (not synced `pytest.ini`, not duplicated `pyproject` tables)**
   - **Choice:** A small Devinfra-owned module registers the fleet marker set in `pytest_configure` (and MAY enable
     `--strict-markers` via plugin/`addopts` only if that does not fight product `addopts`).
   - **Why:** Pytest’s first-match config rules make a markers-only ini unsafe next to product discovery settings. A
     plugin composes with product `pyproject` instead of replacing it.
   - **Alternatives:** Synced root `conftest.py` only (easier, easier to miss/override); keep forever copy-paste (status
     quo; rejected as long-term SoT).

2. **Plugin load path (implement default)**
   - **Choice:** Prefer a discoverable install (workspace / thin package + `pytest11` entry point) so `uv run pytest`
     and pre-push load it without per-product `PYTEST_PLUGINS` env forking. Document `PYTEST_PLUGINS` as a fallback for
     checkouts that cannot take the entry point yet.
   - **Why:** Env-only adopt drifts; silent unload breaks `--strict-markers`. Entry point is the durable fleet path.
   - **Alternatives:** Env-only (smaller first PR, weaker guarantee); root synced `conftest` (no packaging, weaker
     identity as a shared module).

3. **Coverage = linked follow-up, not this design’s implement MVP**
   - **Choice:** Do not design-ship `.coveragerc` / `coverage.toml` composition in the first implement PR. Open a linked
     issue when markers plugin is adopted.
   - **Why:** Different tool, different adopt (`--cov-config` / drop duplicate tables); bundling doubles risk for a
     low-severity / expensive Feature.
   - **Alternatives:** Both in one implement PR (issue AC “full”); coverage-only (does not remove marker duplication).

4. **Product-owned forever**
   - `testpaths`, `pythonpath`, product-specific `filterwarnings` / markers
   - Coverage `source=` (and any product-only omit) when a coverage fragment exists later

5. **This OpenSpec change is design + docs pointer only (`skip_specs: true`)**
   - A future implement change MUST add real delta specs under `shared-python-quality-config` and/or
     `shared-quality-tooling`, add sync allowlist paths, and remove the “deferred” wording from `docs/quality.md`.

## Risks / Trade-offs

- **[Risk] Design drifts before implement** → Keep #123 open; quality.md points at this change name and the locked
  decisions above.
- **[Risk] Implement PR re-litigates entry point vs env** → Decision 2 is the default; change it only with a design
  update, not ad-hoc in code review.
- **[Trade-off] No capability in main specs yet** → Avoids archiving unimplemented requirements; intentional for
  design-only.

## Migration Plan

1. **This PR (design):** Merge proposal/design/tasks + `docs/quality.md` planned-SoT note; leave product marker tables
   as-is.
2. **Later implement PR:** Ship plugin + sync + product adopt notes; strip duplicate fleet markers from product
   `pyproject` once the plugin loads in pre-push/CI; add delta specs; archive that change with sync.
3. **Rollback of design-only:** Revert the docs pointer; products unchanged.
4. **Coverage follow-up:** Separate issue after markers adopt.

## Open Questions

- Exact module path / package name under Devinfra (e.g. `scripts/pytest_plugins/…` vs small `pyproject` member) — decide
  in the implement change without revisiting Decisions 1–3.
- Whether the plugin also sets `--strict-markers` globally or products keep that flag — decide at implement time if
  product `addopts` conflict appears.
