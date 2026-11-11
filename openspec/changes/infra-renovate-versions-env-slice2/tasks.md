# Tasks

## 1. Pin file split and product loaders

- [ ] 1.1 Create `versions.foundation.env` with foundation-eligible pins from design D1 and leave python-product-only
      pins in `versions.env` with no duplicate keys — verify by grepping that each `*_VERSION` key appears in exactly
      one of the two files
- [ ] 1.2 Update `scripts/load-versions-env.sh` to source foundation then `versions.env` and fail closed if either file
      is missing — verify by running the script successfully in this repo and by temporarily renaming each file and
      confirming a clear error
- [ ] 1.3 Wire Compose / Dev Container build-arg loading to consume both pin files (dual `env_file` or documented
      equivalent) — verify `.devcontainer/docker-compose.yml` references both files and docs mention the load path
- [ ] 1.4 Update foundation-pin readers (`scripts/install-gitleaks.sh`, helm pin lookup in `scripts/run-helm-lint.sh`,
      and any other helper that only needs foundation keys) to read `versions.foundation.env` — verify each script
      resolves its pin from the foundation file

## 2. Renovate config for split pins + Infra skip

- [ ] 2.1 Update `renovate.json` regex managers / packageRules so foundation pins use `versions.foundation.env` and
      product pins use `versions.env` — verify no manager targets the same key in both files
- [ ] 2.2 Extend synced-SoT skip rules so products skip both pin files (+ existing paths) and Infra skips
      `versions.foundation.env` + Renovate artifacts — verify `renovate.json` packageRules mention `m4.2_infrastructure`
      and the foundation pin path

## 3. Sync allowlist and profile tests

- [ ] 3.1 Move `renovate.json`, `.github/workflows/renovate.yml`, `docs/renovate.md`, and `versions.foundation.env` onto
      `foundation` in `docs/synced-paths.yaml`; keep `versions.env` / `.python-version` on `python-product` — verify
      `uv run python scripts/sync-products.py --list-files --target infrastructure` includes Renovate + foundation pins
      and excludes `versions.env` / `.devcontainer/**`
- [ ] 3.2 Update `scripts/tests/test_sync_products_profiles.py` for the new membership — verify the profile test file
      passes (`uv run pytest scripts/tests/test_sync_products_profiles.py`)
- [ ] 3.3 Keep `skip_infrastructure` default **true**; document how to dry-run / unskip after the bot checklist — verify
      workflow input default remains true and docs state the ordering

## 4. Docs: checklist, pin buckets, Dependabot plan

- [ ] 4.1 Update `docs/renovate.md` repository-access list + Infra adoption checklist (PAT, Infra secret, sync dry-run /
      unskip, Infra#80 note) and Infra Dependabot wind-down **plan** — verify the doc names Infra and the checklist
      steps
- [ ] 4.2 Update `docs/sync.md` / `docs/devcontainer.md` pin-ownership tables for the two-file split and remove
      “Renovate deferred to #354” wording — verify tables name `versions.foundation.env` vs `versions.env` and Infra
      Renovate via foundation

## Workflow follow-up

- After apply + user commits/push: open draft PR with `Fixes #354`
- Archive this change on the last `go`
- Operators run the bot checklist out-of-band; Infra Dependabot file removal stays on Infra after Renovate is green
