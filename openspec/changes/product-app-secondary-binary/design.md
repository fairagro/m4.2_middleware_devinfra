## Context

See `proposal.md` for motivation ([#71](https://github.com/fairagro/m4.2_middleware_devinfra/issues/71)). Today
`docker/Dockerfile.product-app.base` hard-codes a single `pyinstaller --onedir` for `BINARY_NAME` /
`PYINSTALLER_IMPORT|ENTRY` and exports `/build/dist` → `/dist`. Explore lock-in: **Option A** — one optional secondary
in the same `binary-builder` via `SECONDARY_*` ARGs; empty = no-op; not N secondaries; not primary-as-onefile; harvester
Dockerfile deletion is product follow-up.

## Goals / Non-Goals

**Goals:**

- Backward-compatible optional secondary under `/dist` from the synced base
- Document ARG + last-stage COPY contract; refresh examples lightly
- Delta `shared-product-app-dockerfile` only

**Non-Goals:**

- Removing harvester’s `Dockerfile.harvester-healthcheck` in this repo
- Multiple secondaries, JSON lists, or a second Bake export context as the MVP path
- Changing primary default away from `--onedir`
- Expanding reusable-build / CST beyond documenting new optional args products may pass

## Decisions

### D1: Same binary-builder stage, not a second Bake base target

**Choice:** After the primary `pyinstaller --onedir`, optionally run a second PyInstaller invocation when
`SECONDARY_BINARY_NAME` is non-empty; `export-binaries` still `COPY`s `/build/dist` once.

**Alternatives:** Two Bake `*-base` targets + two last-stage contexts (needs a mode ARG anyway, more product surface);
product-local second Dockerfile (status quo, violates done-when).

### D2: ARG surface

| ARG                            | Role                                                                     |
| ------------------------------ | ------------------------------------------------------------------------ |
| `SECONDARY_BINARY_NAME`        | Gate + `--name`; empty → skip secondary entirely                         |
| `SECONDARY_PYINSTALLER_IMPORT` | Preferred entry resolution (same `main.py` pattern as primary)           |
| `SECONDARY_PYINSTALLER_ENTRY`  | Optional path override after wheel install                               |
| `SECONDARY_ONEFILE`            | Default `true` when secondary runs; set `false` for secondary `--onedir` |

Ignore other `SECONDARY_*` when the name is empty. Fail closed if name set but neither import nor valid entry resolves.

### D3: Docs + examples, not workflow changes

Document in `docs/ci.md` and comment/args in the base header. Extend `docker/examples/` with commented secondary args
and an optional COPY line for a onefile secondary. Do not change `reusable-build.yml` matrix semantics — products
already pass component-specific Bake args.

## Risks / Trade-offs

- **[Risk] Last-stage path confusion** (onedir tree vs onefile file) → Mitigation: document `/dist/<name>/` vs
  `/dist/<name>` and show both in examples
- **[Risk] Products set name without import** → Mitigation: fail closed with a clear ERROR line (same style as primary)
- **[Risk] Layer cache invalidation** when secondary args change → Acceptable; secondary is rare and intentional

## Migration Plan

1. Land base + docs + examples on the issue branch; draft PR `Fixes #71`.
2. After merge/sync, harvester (and any peer) adopts secondary ARGs and deletes product-local healthcheck Dockerfile in
   a product PR (linked follow-up / `SYNC-FOLLOWUP` as needed — out of this change).

## Open Questions

None — explore lock-ins applied (Option A, one secondary, default onefile for secondary).
