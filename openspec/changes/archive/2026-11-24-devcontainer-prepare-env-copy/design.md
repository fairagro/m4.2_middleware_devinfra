## Context

See `proposal.md`. Compose reads `.devcontainer/.env` before image build; postCreate is too late.

## Goals / Non-Goals

**Goals:**

- Reliable Compose pin substitution on `core.symlinks=false` checkouts
- Single committed pin file: `versions.env`
- Host prepare before Compose via `initializeCommand`

**Non-Goals:**

- Changing which pins live in `versions.env`
- Infra GitOps Dev Container (not on this blob)
- Making bare `docker compose` without prepare a supported happy path

## Decisions

1. **`rm -f` then `cp`** — unlinks a symlink; avoids writing through a symlink into `versions.env`.
2. **`initializeCommand` on host** — runs before Compose; required for build-args.
3. **Stop tracking `.devcontainer/.env`** — generated artifact; gitignore via existing `.env` rules after dropping
   `!.devcontainer/.env`.
4. **Keep Renovate `ignorePaths` entry** — local copy must not be scanned as a second pin file.

## Risks / Trade-offs

- [Bare compose without prepare] → Empty pins; docs say open via Dev Containers or run the script first.
- [Stale copy if versions.env edited without re-prepare] → Next Dev Container reopen / rebuild re-runs
  initializeCommand.

## Migration Plan

1. Land script + JSON + gitignore + docs + specs; remove tracked symlink.
2. Sync to products; reopen Dev Containers once.

## Open Questions

None.
