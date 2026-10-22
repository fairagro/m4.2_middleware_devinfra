## Context

See proposal.md — Why. Today commitlint only validates the Conventional Commits type token. Agent handoff subjects (#319
/ #321) reduce bad drafts but do not stop unread sparkle. Explore lock-in: option **A** — dedicated script + commit-msg
hook beside commitlint.

## Goals / Non-Goals

**Goals:**

- Fail closed on `feat`/`fix` vs OpenSpec-only / archive+spec-sync / test-only indexes
- Reject `docs` for archive commits in favour of `chore(openspec)`
- Syncable script + pre-commit entry; docs + fixtures

**Non-Goals:**

- Replacing commitlint or agent handoff Suggested messages
- Hiding Cursor/VS Code generate buttons
- Perfect NLP subject quality on real product diffs
- Blocking `--no-verify`

## Decisions

1. **Shell script `scripts/commit-path-check.sh`** — Invoked from `.pre-commit-config.yaml` `stages: [commit-msg]` with
   the message file path (same pattern as commitlint `--edit`). Parses first non-comment line for `type(scope)!:`.
   Alternative rejected: commitlint plugin (weak staged-path access).

2. **Path buckets** — Classify each staged path into: `openspec_planning`, `openspec_archive`, `openspec_specs`, `test`,
   `other`. Reject matrix uses set logic (all staging in {planning}; all in {archive,specs}; all in {test}).

3. **Test globs** — Path contains `/tests/` or `/test/`, or basename matches `test_*.py`, `*_test.py`, `*_test.go`,
   `*.test.ts`, `*.spec.ts` (document list; keep conservative). Mixed test+product → allow `feat`/`fix`.

4. **Archive `docs` → reject** — If type is `docs` and staged set ⊆ {archive, specs} with at least one archive path →
   fail with hint to use `chore(openspec)`.

5. **Allowlist** — Add script to `docs/synced-paths.yaml` / sync.md; `.pre-commit-config.yaml` already synced.

6. **Fixtures** — Small shell or Python tests under `scripts/` that invoke the checker with temp repos or mocked path
   lists / message strings (prefer pure functions + CLI flags for testability if needed).

## Risks / Trade-offs

- [Over-broad test globs] → Mitigation: document patterns; only pure-test indexes reject
- [Commit with both archive and product] → Allow `feat`/`fix` (shipped paths present)
- [Hook order vs commitlint] → Both commit-msg; either order OK; path-check should not depend on commitlint passing
- [`--no-verify`] → Document as escape; not a control

## Migration Plan

1. Land script + hook + docs in Devinfra
2. Sync to products; existing hooks reinstall on next postCreate / `pre-commit install --hook-type commit-msg`
3. Rollback: remove hook entry / script from sync
