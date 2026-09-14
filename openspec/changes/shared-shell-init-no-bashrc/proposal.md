## Why

Product repos still ship near-duplicate `scripts/load-env.sh` wired through `~/.bashrc` for `.venv` on `PATH`,
kubectl/docker shortcuts, and optional SOPS decrypt. Devinfra intentionally stopped patching bashrc for personal tokens,
but never replaced the rest of that shell-init job — copies drift and conflict with “never hand-edit synced blobs.” Wave
B needs a **bashrc-free** fleet contract so every interactive Dev Container shell gets the same happy path without
home-profile mutation.

## What Changes

- Document and require product/Devinfra `devcontainer.json` `remoteEnv.PATH` to prepend **both**
  `${workspaceFolder}/.venv/bin` and `${workspaceFolder}/scripts/bin` (no `~/.bashrc` patch for PATH).
- Add synced `scripts/bin` wrappers for kubectl/docker shortcuts (replace bash aliases from product `load-env.sh`).
- Extend shared `scripts/devcontainer-post-create.sh` to optionally decrypt repo-root `.env.integration.enc` → `.env`
  when present (write the file; do **not** auto-export into every shell). Soft-fail when SOPS/keys missing.
- Docs: remove guidance that implies bashrc/`load-env.sh` is the fleet pattern; point products at remoteEnv + wrappers +
  postCreate decrypt; note that product adopt (drop load-env/bashrc) is **out of this PR** via follow-up issues.
- **Do not** add `scripts/load-env.sh` or `setup-bashrc-load-env.sh`.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `shared-devcontainer-base`: bashrc-free shell PATH contract, kubectl/docker wrappers, optional postCreate SOPS decrypt
  to `.env`, consumer docs for product adopt without `load-env.sh`.

## Impact

- `.devcontainer/devcontainer.json` (Devinfra overlay), `scripts/bin/*`, `scripts/devcontainer-post-create.sh`,
  `docs/synced-paths.yaml`, `docs/devcontainer.md` / conventions pointers, OpenSpec main sync on archive.
- Product repos: **not** migrated in this change — follow-up issues per consumer to drop bashrc/`load-env.sh` and align
  `remoteEnv`.
- Personal-token helpers stay as today (`scripts/bin/gh|git`, `dev-tokens.sh`); no bashrc for tokens.
