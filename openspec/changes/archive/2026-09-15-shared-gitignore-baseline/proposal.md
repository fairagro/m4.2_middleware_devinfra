## Why

Product repos duplicate large Python/tooling `.gitignore` lists while Devinfra keeps a tiny stub. Wave B already needs
shared ignores (`node_modules/`, `.devcontainer/.env` symlink exception). That baseline belongs in Devinfra and on the
sync allowlist (#62), with product-only paths kept out of the shared file.

## What Changes

- Expand root `.gitignore` into a **fleet baseline** (Python/uv caches, Node, env secrets with documented exceptions,
  common editor/OS noise) — **verbatim** sync into products.
- **BREAKING (product adopt):** root `.gitignore` becomes synced SoT; products MUST NOT keep forked root ignore lists.
  Product-only paths (e.g. helm TLS scratch, demo output) live in **nested** `.gitignore` files sync does not overwrite.
- Allowlist root `.gitignore` in `docs/synced-paths.yaml`; document overlay pattern in `docs/sync.md`.
- Fix stale AC naming (`synced-paths.yaml`, not `synced-paths.global.md`).

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `synced-consumer-paths`: allowlist MUST include root `.gitignore`; docs MUST describe nested product ignore overlays.

## Impact

- Root `.gitignore`, `docs/synced-paths.yaml`, `docs/sync.md` (and brief quality/conventions pointer if needed).
- Product adopt: replace root boilerplate with synced file; move deltas to nested ignores (follow-up product issues as
  needed).
