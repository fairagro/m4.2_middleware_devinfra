# Tasks

## 1. Sync allowlist + Renovate Infra skip

- [x] 1.1 Move `renovate.json`, `.github/workflows/renovate.yml`, `docs/renovate.md`, and `versions.env` onto
      `foundation` in `docs/synced-paths.yaml`; keep `.python-version` / Dev Container on `python-product` — verify
      `uv run python scripts/sync-products.py --list-files --target infrastructure` includes Renovate + `versions.env`
      and excludes `.devcontainer/**` / `.python-version`
- [x] 1.2 Extend `renovate.json` synced-SoT skip so Infra skips `versions.env` + Renovate artifacts — verify
      `m4.2_infrastructure` appears in packageRules with those paths
- [x] 1.3 Update `scripts/tests/test_sync_products_profiles.py` for the new membership — verify
      `uv run pytest scripts/tests/test_sync_products_profiles.py` passes
- [x] 1.4 Keep `skip_infrastructure` default **true**; document dry-run / unskip after the bot checklist — verify
      workflow input default remains true

## 2. Docs: checklist, pin buckets, Dependabot plan

- [x] 2.1 Update `docs/renovate.md` repository-access list + Infra adoption checklist and Dependabot wind-down **plan**
      — verify the doc names Infra and states unused pins are no-ops
- [x] 2.2 Update `docs/sync.md` / `docs/devcontainer.md` for foundation Renovate + single `versions.env` (no file split)
      — verify tables no longer say Renovate is deferred to #354

## Workflow follow-up

- After apply + user commits/push: open draft PR with `Fixes #354`
- Archive this change on the last `go`
- Operators run the bot checklist out-of-band; Infra Dependabot file removal stays on Infra after Renovate is green
