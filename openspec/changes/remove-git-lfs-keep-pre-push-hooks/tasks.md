# Tasks: remove Git LFS, keep pre-push quality hooks

## 1. Hooks and installer

- [ ] 1.1 Add `scripts/setup-git-hooks.sh` (copy `pre-push` only; no git-lfs)
- [ ] 1.2 Replace `scripts/setup-git-lfs.sh` with a thin stub directing to `setup-git-hooks.sh`
- [ ] 1.3 Rewrite `scripts/git-hooks/pre-push` without LFS; delete `post-checkout` / `post-commit` / `post-merge`
- [ ] 1.4 Point `scripts/devcontainer-post-create.sh` at `setup-git-hooks.sh`

## 2. Dev Container image

- [ ] 2.1 Remove `git-lfs` and `git lfs install --system` from `.devcontainer/Dockerfile`

## 3. Docs

- [ ] 3.1 Update README, `docs/quality.md`, `docs/devcontainer.md` (hooks-only install; product-local LFS note for
      sql-to-arc / sync #13)

## 4. Validate

- [ ] 4.1 `openspec validate remove-git-lfs-keep-pre-push-hooks --strict`
- [ ] 4.2 `npm run format:md` and `npm run lint:md` on touched Markdown
