# Remove Git LFS from shared Devinfra (keep pre-push hooks)

## Why

Shared Devinfra installs and hooks **Git LFS** even though this repo (and most products) do not use LFS as a content
store. LFS is coupled to installing the useful **pre-push quality** git hook. Remove LFS from the shared image and hooks
while keeping the pre-commit pre-push quality gate. Products that need LFS (e.g. sql-to-arc) install it product-locally
after sync.

## What Changes

- Drop `git-lfs` / `git lfs install --system` from the shared Dev Container Dockerfile (**D1**)
- Replace `scripts/setup-git-lfs.sh` with `scripts/setup-git-hooks.sh` (hooks only); **delete** the old script name
  (no stub)
- Slim `scripts/git-hooks/pre-push` to pre-commit pre-push only; delete LFS-only `post-*` hooks (**C1**)
- postCreate calls `setup-git-hooks.sh`
- Rename OpenSpec capability `shared-git-hooks-lfs` → `shared-git-hooks` (**A1**); update `shared-devcontainer-base` and
  `shared-quality-tooling`
- Docs: README, quality, devcontainer — no shared LFS requirement; note product-local LFS for repos that need it (#13 /
  sql-to-arc)

## Capabilities

### New Capabilities

- `shared-git-hooks`: Version-controlled git hooks installer and pre-push quality hook **without** Git LFS

### Modified Capabilities

- `shared-git-hooks-lfs`: Retire capability (all requirements removed; migrate to `shared-git-hooks`)
- `shared-devcontainer-base`: Shared image and postCreate no longer install Git LFS; postCreate uses
  `setup-git-hooks.sh`; document product-local LFS when needed
- `shared-quality-tooling`: Install docs point at `setup-git-hooks.sh` / hooks-only pre-push

## Impact

- `.devcontainer/Dockerfile`, `scripts/setup-git-hooks.sh`, `scripts/git-hooks/`,
  `scripts/devcontainer-post-create.sh`
- Docs + README; OpenSpec specs above
- Sync (#13): consumers migrate installer name; sql-to-arc (and any LFS user) adds product-local `git-lfs`
- Issue: [#39](https://github.com/fairagro/m4.2_middleware_devinfra/issues/39)
