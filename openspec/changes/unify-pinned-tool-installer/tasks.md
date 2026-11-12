## 1. Driver + delete per-tool installers

- [ ] 1.1 Add `scripts/install-pinned-tool.sh` with bash `case` registry for `gitleaks`, `actionlint`, `kubeconform`,
      `cst`, `git-cliff` (pin env, asset/URL, arch map, extract/install, optional checksum, version check; sudo-safe
      `versions.env` load; fail closed on missing pin/unknown id) — verify each tool id installs under `INSTALL_DIR`
      override in Dev Container
- [ ] 1.2 Delete `scripts/install-{gitleaks,actionlint,kubeconform,cst,git-cliff}.sh` (no shims) — verify repo has no
      remaining `scripts/install-<tool>.sh` for those five

## 2. Call sites + sync allowlist

- [ ] 2.1 Update reusable workflow install steps and `scripts/devcontainer-post-create.sh` to
      `bash scripts/install-pinned-tool.sh <tool>` (keep one step per tool; preserve `sudo` where used) — verify grep
      shows no old script paths outside archive/history
- [ ] 2.2 Allowlist `scripts/install-pinned-tool.sh` (foundation); remove the five old install paths from
      `docs/synced-paths.yaml`; keep `scripts/run-kubeconform.sh` — verify profile tests pass

## 3. Docs + validate

- [ ] 3.1 Update `docs/quality.md` / `docs/ci.md` (+ sync inventory as needed): driver usage, dual path Dockerfile
      inline vs driver, link [#374](https://github.com/fairagro/m4.2_middleware_devinfra/issues/374) — verify Prettier
      on touched Markdown
- [ ] 3.2 `openspec validate unify-pinned-tool-installer --strict` + Prettier on change Markdown — verify validate
      succeeds

## Workflow follow-up

- Draft PR after apply commits; archive on final issue-fixer `go`
- Dockerfile-via-driver remains [#374](https://github.com/fairagro/m4.2_middleware_devinfra/issues/374)
