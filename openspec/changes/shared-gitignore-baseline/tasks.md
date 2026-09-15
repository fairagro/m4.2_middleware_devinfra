## 1. Baseline file

- [x] 1.1 Expand root `.gitignore` to fleet baseline (Python/uv/tool caches, Node, env + documented exceptions, light
      editor/OS); exclude product-only helm/demo paths
- [x] 1.2 Keep `!.devcontainer/.env` (and `!.env.integration.enc` if still required) documented in-file

## 2. Sync + docs

- [x] 2.1 Allowlist `.gitignore` in `docs/synced-paths.yaml`
- [x] 2.2 Document nested product ignore overlays + inventory in `docs/sync.md`

## 3. Validate

- [x] 3.1 `openspec validate --strict`; format/lint Markdown
