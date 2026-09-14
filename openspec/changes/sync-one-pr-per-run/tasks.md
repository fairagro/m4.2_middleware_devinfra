# Tasks: sync-one-pr-per-run

## 1. Script: SHA-scoped branch and new PR

- [x] 1.1 Replace fixed `SYNC_BRANCH` with `chore/devinfra-sync-<shortsha>` derived from `source_sha`
- [x] 1.2 Push the new branch without `--force`; keep shallow clone + full allowlist copy behavior
- [x] 1.3 Always create a new PR when there are changes (remove “update existing PR via force-push” path)

## 2. Script: Supersede older open sync PRs

- [x] 2.1 After the new PR is created, list other open PRs whose head starts with `chore/devinfra-sync`
- [x] 2.2 Comment `Superseded by #<new>…` and close those PRs without merging (skip dry-run)
- [x] 2.3 Only run supersede after successful new-PR creation; never close the new PR

## 3. Docs and verify

- [x] 3.1 Update `docs/sync.md` for one-PR-per-run, branch naming, and supersede (no auto-merge)
- [x] 3.2 Run a local `--dry-run` (and `--list-files` if useful) to confirm no PR side effects
- [x] 3.3 Format/lint touched Markdown (`npm run format:md` / `npm run lint:md` as needed)
