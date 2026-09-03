# Bootstrap repo layout — Proposal

## Why

This repo is meant to be the shared source of truth for three m4.2 product repos, but it still has no root README, no
documented ownership model, and no placeholder layout for the paths later extraction issues will fill. Issue #2 is the
first epic step: make the repo usable as that canonical home before copying shared files.

## What Changes

- Add a root `README.md` stating purpose, consumer repos, ownership (edit here first; consumers must not hand-edit
  synced paths), a short note on `versions.env` / `.python-version`, and links into `docs/`
- Add `docs/devcontainer.md` as the first feature doc (Dev Container operator guide), relocating and rewriting content
  currently in `.devcontainer/README.md`
- **Delete** `.devcontainer/README.md` (no pointer stub left behind)
- Add empty directory skeleton with `.gitkeep`: `docs/` (alongside the real doc), `.agents/skills/`, `.cursor/`,
  `.github/`
- Leave existing `.devcontainer/` tooling files and `scripts/` as-is aside from the README deletion

## Capabilities

### New Capabilities

- `repo-layout`: Canonical shared-Devinfra repo presentation — root README contract, docs index pattern, directory
  skeleton, and where Dev Container / tool-version documentation lives

### Modified Capabilities

- (none — no main specs exist yet)

## Impact

- Human and agent entry point becomes root `README.md` + `docs/`, not `.devcontainer/README.md`
- Later epic issues (#3–#16) land into the skeleton paths without inventing layout
- No product code, no sync automation, no path-convention lock-in (#3), no OpenSpec trees for product repos
- Existing Dev Container image and `versions.env` behavior unchanged; only documentation location and framing change
