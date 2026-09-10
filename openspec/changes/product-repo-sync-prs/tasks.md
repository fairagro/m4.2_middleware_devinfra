# Tasks: product-repo sync PRs

## 1. Allowlist SoT

- [x] 1.1 Expand `docs/synced-paths.yaml` with concrete quality/DC/hooks/scripts paths; document hard excludes
      (middleware, openspec specs/changes, reusable-*.yml, overlays)
- [x] 1.2 State in the allowlist (and synced-consumer-paths intent) that this file is the sole sync path list

## 2. Sync automation

- [x] 2.1 Add sync script that parses the allowlist, expands globs, applies hard excludes, copies into target worktrees
- [x] 2.2 Add `.github/workflows/sync-products.yml`: push to `main` (live PRs) + `workflow_dispatch` dry-run/skip
      inputs; bot token secret
- [x] 2.3 Wire three targets (API, sql-to-arc, harvester); open/update sync PRs via `gh`

## 3. Docs and Renovate token alignment

- [x] 3.1 Add `docs/sync.md` (triggers, dry-run/skip, token, allowlist, excludes); link from README / ci
- [x] 3.2 Update `docs/renovate.md` for shared bot token with sync

## 4. Validate

- [x] 4.1 Dry-run locally or via dispatch against at least one target when token available; otherwise document
- [x] 4.2 Format/lint Markdown; spot-check workflow never copies excluded trees
