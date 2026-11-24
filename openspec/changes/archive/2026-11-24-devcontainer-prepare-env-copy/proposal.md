# Proposal

## Why

On checkouts with `core.symlinks=false` (Windows / many WSL mounts), the tracked `.devcontainer/.env` →
`../versions.env` symlink is not a real symlink. Compose then interpolates empty or stale pins before the image build.
[`#410`](https://github.com/fairagro/m4.2_middleware_devinfra/issues/410) replaces the symlink with a host-side
generated copy of `versions.env` via `initializeCommand`, before Compose runs.

## What Changes

- Add `scripts/devcontainer-prepare-env.sh` (`rm -f` + `cp versions.env` → `.devcontainer/.env`); allowlist on
  `python-product`
- Wire `.devcontainer/devcontainer.json` `initializeCommand` to that script
- Stop tracking `.devcontainer/.env`; drop `!.devcontainer/.env` gitignore exception
- Keep `versions.env` as the only committed pin file; Renovate still ignores `.devcontainer/.env`
- Docs/comments: generated copy, not symlink (`docker-compose.yml`, `devcontainer.md`, `renovate.md`, `versions.env`)
- OpenSpec `shared-devcontainer-base`: Compose build-args via generated `.env` copy + host `initializeCommand`

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `shared-devcontainer-base`: `.devcontainer/.env` is a generated copy of `versions.env` prepared on the host before
  Compose build; no tracked symlink

## Impact

Synced product Dev Containers; WSL/`core.symlinks=false` checkouts get correct Compose pins. Contributors must open via
Dev Containers (or run the prepare script) before a bare `docker compose` build that expects `.devcontainer/.env`.
