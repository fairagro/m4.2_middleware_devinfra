# Tasks: remove Git LFS, keep pre-push quality hooks

## 1. Hooks and installer

- [x] 1.1 Add `scripts/setup-git-hooks.sh` (copy `pre-push` only; no git-lfs)
- [x] 1.2 Remove `scripts/setup-git-lfs.sh` (no stub; only `setup-git-hooks.sh`)
- [x] 1.3 Rewrite `scripts/git-hooks/pre-push` without LFS; delete `post-checkout` / `post-commit` / `post-merge`
- [x] 1.4 Point `scripts/devcontainer-post-create.sh` at `setup-git-hooks.sh`

## 2. Dev Container image

- [x] 2.1 Remove `git-lfs` and `git lfs install --system` from `.devcontainer/Dockerfile`

## 3. Docs

- [x] 3.1 Update README, `docs/quality.md`, `docs/devcontainer.md` (hooks-only install; product-local LFS note for
      sql-to-arc / sync #13)

## 4. Validate

- [x] 4.1 `openspec validate remove-git-lfs-keep-pre-push-hooks --strict`
- [x] 4.2 `npm run format:md` and `npm run lint:md` on touched Markdown
