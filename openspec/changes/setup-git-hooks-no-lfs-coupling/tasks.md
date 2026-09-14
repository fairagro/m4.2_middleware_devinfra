## 1. Shared hook installer

- [ ] 1.1 Remove LFS detection/deletion loop and LFS-specific messaging from `scripts/setup-git-hooks.sh` (quality
      `pre-push` only)
- [ ] 1.2 Confirm `scripts/devcontainer-post-create.sh` does not invoke product scripts (`install-dev-hooks.sh` /
      `setup-git-lfs.sh`)

## 2. Docs

- [ ] 2.1 Update `docs/devcontainer.md` LFS wording (product-owned; no synced JSON postCreate snippet; no shared
      product-script callback)
- [ ] 2.2 Update `docs/quality.md`: LFS product-owned; Mypy/`MYPYPATH` overlays via `product.env` / CI (not `remoteEnv`)

## 3. Spec sync for apply

- [ ] 3.1 Apply deltas into `openspec/specs/shared-git-hooks/spec.md` and
      `openspec/specs/shared-devcontainer-base/spec.md`
- [ ] 3.2 Run `openspec validate setup-git-hooks-no-lfs-coupling --strict` and `npm run format:md` / `npm run lint:md`
      on touched Markdown
