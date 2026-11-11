## 1. Allowlist YAML profiles

- [ ] 1.1 Restructure `docs/synced-paths.yaml` to `profiles.foundation` / `profiles.python-product`, shared
      `exclude`/`overlays`, and `targets` (api/sql_to_arc/harvester → both profiles; infrastructure → foundation);
      verify YAML parses and foundation membership matches lock-in (skills incl. uv, commands/prompts, skill docs,
      `scripts/ai/**`, `m42-ai`, token helpers) with Renovate/devcontainer/pre-commit only under python-product
- [ ] 1.2 Update `docs/sync.md` (and README link text if needed) for profiles, fourth target, dry-run/skip, Slice-1
      non-goals; verify docs name `infrastructure` and foundation-only scope

## 2. Sync implementation

- [ ] 2.1 Update `scripts/sync-products.py` to load profiles/targets from YAML, resolve per-target effective allow,
      per-target orphans, `--skip-infrastructure`, and `--list-files` defaulting to product union (optional `--target`);
      verify `--list-files` and a dry-run listing for `infrastructure` vs `api` differ as expected
- [ ] 2.2 Update `.github/workflows/sync-products.yml` inputs/steps for `skip_infrastructure` and docs comments; verify
      workflow YAML still validates (`actionlint` if available, else schema/manual review)
- [ ] 2.3 Extend or add unit/integration tests under `scripts/` for profile union and foundation-only Infra resolve;
      verify tests pass with `uv run pytest` on the touched test module(s)

## 3. Validate

- [ ] 3.1 Run `openspec validate sync-foundation-profile-slice1 --strict` and fix deltas; verify exit 0
- [ ] 3.2 Prettier/markdownlint on touched Markdown; verify clean for changed paths
