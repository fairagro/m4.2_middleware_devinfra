## 1. Install helper + workflow

- [ ] 1.1 Add `scripts/install-cst.sh` (read `CST_VERSION` from `versions.env`, fail closed, install official
      linux-amd64 binary; optional `cst` symlink) — verify `--help`/missing pin behaviour locally
- [ ] 1.2 Replace `plexsystems/container-structure-test-action` in `reusable-check.yml` with install + CLI `test`
      invocation — verify step order still has checkout + loaded image

## 2. Sync + docs

- [ ] 2.1 Allowlist `scripts/install-cst.sh` in `docs/synced-paths.yaml` / `docs/sync.md`
- [ ] 2.2 Update `docs/ci.md`: CI CST follows `versions.env` / Renovate — verify Prettier/markdownlint

## 3. Validate

- [ ] 3.1 Run `openspec validate cst-version-ci --strict` — verify exit 0
