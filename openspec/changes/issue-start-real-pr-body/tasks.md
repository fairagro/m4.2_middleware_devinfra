## 1. CLI

- [ ] 1.1 Implement default PR body builder (issue title + capped `git log` subjects + `Fixes #<n>`; never `(fill in)`)
      and verify with a unit/contract test that the composed body matches
- [ ] 1.2 Add `--body` / `--body-file` to `issue-start`; append `Fixes #<n>` when missing; verify override test covers
      append-and-use paths
- [ ] 1.3 Wire CLI args through `cli.py`; verify `--help` lists the new flags

## 2. Skills and docs

- [ ] 2.1 Update `/issue-fixer` skill (+ thin `docs/issue-fixer.md` / README as needed) to prefer `--body-file` with
      real bullets and drop the fill-in stub example; verify no skill text still presents `(fill in)` as intended

## 3. Verification

- [ ] 3.1 Run `openspec validate issue-start-real-pr-body --strict` and `uv run --project scripts/ai pytest` for
      affected issue-start tests; confirm both pass
