## 1. Shared Dev Container entry files

- [ ] 1.1 Update `.devcontainer/devcontainer.json`: `workspaceFolder` `/workspace`, `name` and volume `source=` from
      `${localWorkspaceFolderBasename}`; keep shared PATH/extensions/postCreate; no product-only remoteEnv
- [ ] 1.2 Update `.devcontainer/docker-compose.yml`: bind `..:/workspace:cached`; add optional
      `.devcontainer/product.env` via Compose `env_file` with `required: false` (verify DinD Compose supports it; else
      document empty-file fallback)
- [ ] 1.3 Rebuild or `devcontainer` config sanity: workspace path and name substitution match the contract (no product
      path hardcoding left in these two files)

## 2. Sync allowlist and docs

- [ ] 2.1 Move `.devcontainer/devcontainer.json` and `.devcontainer/docker-compose.yml` from `exclude` to `allow` in
      `docs/synced-paths.yaml`
- [ ] 2.2 Update `docs/devcontainer.md`, `docs/sync.md`, and `docs/conventions.md`: verbatim JSON+Compose, `/workspace`,
      basename window/volumes, optional `product.env`; remove thin-overlay / “product-owned until #65” wording
- [ ] 2.3 Update `openspec/specs/shared-devcontainer-base/spec.md` Purpose to match the new contract (delta archives
      requirements; Purpose is edited on the main spec)

## 3. Validate

- [ ] 3.1 `openspec validate shared-devcontainer-json-workspace --strict`
- [ ] 3.2 Format/lint touched Markdown (`npm run format:md` / `npm run lint:md` as needed)
