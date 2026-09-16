## 1. m42-ai sync-followup plumbing

- [ ] 1.1 Add `pr-for-commit` (or equivalent) to resolve a Devinfra PR for a SHA; verify with a unit/contract test using
      mocked `gh` JSON
- [ ] 1.2 Add trailer parsing for `SYNC-FOLLOWUP: <id>` from PR body **and** comments (ignore malformed / PENDING
      drafts); verify tests cover body-only, comment-only, and both
- [ ] 1.3 Add `sync-followup-ensure` create-or-reuse (Task, `severity:low`, cost default, dedupe label
      `sync-followup:<id>`, template body with source link); verify reuse vs create with mocked `gh`
- [ ] 1.4 Wire CLI subcommands + help text; verify `uv run m42-ai … --help` lists them and `uv run pytest` for
      `scripts/ai` passes

## 2. Sync orphan delete + orchestration

- [ ] 2.1 Extend allowlist listing to resolve file sets at a given git ref / base; verify `--list-files` (or equivalent)
      differs across two refs in a dry check
- [ ] 2.2 In `sync-products.py`, after copy, `git rm` paths in `list(base) − list(HEAD)` that exist in the product clone
      when `--orphan-base` / workflow `before` is set; verify dry-run prints would-delete paths and a local
      fixture/integration path covers delete+commit intent
- [ ] 2.3 Invoke `m42-ai` follow-up ensure from workflow and/or sync script for trailer ids + dispatch input; verify
      dry-run does not create issues (scripted or documented dry path)

## 3. Workflow + docs + permissions

- [ ] 3.1 Update `.github/workflows/sync-products.yml`: pass orphan base on push; add follow-up id dispatch input; call
      ensure for collected ids; verify workflow YAML parses (`actionlint` if available, else visual + `python -c yaml`)
- [ ] 3.2 Update `docs/sync.md` (delete delta, trailer body+comments, dispatch, author/agent checklist) and note Issues
      write on bot if needed in `docs/renovate.md`; verify `npm run format:md` / `npm run lint:md` on touched docs
- [ ] 3.3 `openspec validate sync-orphan-rm-followup --strict` passes

## 4. Agent hint (optional thin)

- [ ] 4.1 Add a short Devinfra-PR note in `docs/sync.md` (and optionally one sentence in issue-fixer Package-adjacent /
      sync section only if it stays accurate when synced): put `SYNC-FOLLOWUP: <id>` on the PR when product follow-ups
      are needed; verify docs lint clean
