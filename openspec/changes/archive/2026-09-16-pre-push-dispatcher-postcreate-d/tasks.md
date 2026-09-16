## 1. Shared git-hooks SoT + installer

- [x] 1.1 Split `scripts/git-hooks/pre-push` into dispatcher + `scripts/git-hooks/pre-push.d/50-quality` (move current
      quality body into the fragment) and verify both files are executable in the tree
- [x] 1.2 Update `scripts/setup-git-hooks.sh` to install/refresh only `.git/hooks/pre-push` and
      `.git/hooks/pre-push.d/50-quality`, leaving foreign `pre-push.d/*` and non-`pre-push` hooks alone; verify a dry
      run in this worktree shows dispatcher + `50-quality` and that a throwaway foreign fragment survives a second run
- [x] 1.3 Verify dispatcher buffers stdin once and runs `pre-push.d/*` in lexicographic order (manual or small shell
      smoke: echo a fake fragment that records order)

## 2. postCreate drop-ins

- [x] 2.1 Append T-late `scripts/devcontainer-post-create.d/*` runner to `scripts/devcontainer-post-create.sh` with
      nullglob skip when empty and hard-fail on non-executable or non-zero; verify by reading the script that it runs
      after shared hook install / remaining shared steps and does not hard-code LFS script names

## 3. Docs + sync awareness

- [x] 3.1 Update `docs/quality.md` and `docs/devcontainer.md` for dispatcher+`.d`, numbering, C2 drop-ins, and product
      LFS adopt notes; verify `npm run format:md` and `npm run lint:md` pass on touched docs/openspec Markdown
- [x] 3.2 Confirm `scripts/git-hooks/**` remains on the sync allowlist and that `scripts/devcontainer-post-create.d/` is
      **not** added as a synced blob (product-owned); verify against `docs/synced-paths.yaml`

## 4. Validate OpenSpec change

- [x] 4.1 Run `openspec validate pre-push-dispatcher-postcreate-d --strict` and fix any reported issues
