# shared-git-hooks-lfs Delta

## REMOVED Requirements

### Requirement: Setup script installs local LFS and project hooks

**Reason**: Shared Devinfra no longer ships or requires Git LFS; hooks-only installer lives under `shared-git-hooks`.

**Migration**: Use `scripts/setup-git-hooks.sh` and capability `shared-git-hooks`. Products that need LFS install
`git-lfs` product-locally.

### Requirement: pre-push runs LFS then pre-commit pre-push stage

**Reason**: Pre-push no longer invokes Git LFS.

**Migration**: See `shared-git-hooks` requirement “pre-push runs pre-commit pre-push stage only”.

### Requirement: LFS lifecycle hooks are version-controlled

**Reason**: LFS-only `post-checkout` / `post-commit` / `post-merge` wrappers are deleted.

**Migration**: None in shared Devinfra; product LFS users rely on `git lfs install` locally if they need LFS hooks.

### Requirement: Documentation of commit vs pre-push install

**Reason**: Docs rewritten under `shared-git-hooks` without LFS.

**Migration**: Follow `shared-git-hooks` documentation requirement.

### Requirement: Dev Container postCreate invokes setup-git-lfs

**Reason**: postCreate invokes `setup-git-hooks.sh` instead.

**Migration**: See `shared-git-hooks` requirement “Dev Container postCreate invokes setup-git-hooks”.
