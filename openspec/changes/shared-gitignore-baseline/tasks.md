## 1. Baseline file

- [ ] 1.1 Expand root `.gitignore` to fleet baseline (Python/uv/tool caches, Node, env + documented exceptions, light
      editor/OS); exclude product-only helm/demo paths
- [ ] 1.2 Keep `!.devcontainer/.env` (and `!.env.integration.enc` if still required) documented in-file

## 2. Sync + docs

- [ ] 2.1 Allowlist `.gitignore` in `docs/synced-paths.yaml`
- [ ] 2.2 Document nested product ignore overlays + inventory in `docs/sync.md`

## 3. Validate

- [ ] 3.1 `openspec validate --strict`; format/lint Markdown
