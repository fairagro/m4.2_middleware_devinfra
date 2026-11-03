## Context

See proposal.md — Why. Locked scope: **A** — `scripts/install-cst.sh` + replace
`plexsystems/container-structure-test-action` in `reusable-check.yml` (#331).

## Goals / Non-Goals

**Goals**

- CI CST binary tracks caller `CST_VERSION`; fail closed; document; syncable install script

**Non-Goals**

- Changing CST YAML configs or component matrices
- Product-vendored local check mirrors in this PR (post-merge sync)
- Pinning Renovate Action / other CLI mismatches

## Decisions

1. **Install script** — Mirror `scripts/install-git-cliff.sh`: source `versions.env` directly (not
   `load-versions-env.sh`), fail if `CST_VERSION` empty, curl
   `https://github.com/GoogleContainerTools/container-structure-test/releases/download/${CST_VERSION}/container-structure-test-linux-amd64`
   into `/usr/local/bin` (same URL as Dev Container Dockerfile). Optional `cst` symlink. Support `CST_INSTALL_DIR`
   override for tests if useful; keep MVP simple.
2. **Workflow** — Keep existing checkout + artifact load. Replace Action step with `sudo bash scripts/install-cst.sh`
   then `container-structure-test test --image local/… --config docker/container-structure-tests/<component>.yaml`.
3. **Sync** — Add script to `docs/synced-paths.yaml` / `docs/sync.md` (callers need it when using shared check).
4. **Docs** — Note beside Trivy binary-pin prose in `docs/ci.md`.

## Risks / Trade-offs

- **[Risk] No published sha512 on all CST releases** → Match Dev Container (curl + chmod); skip checksum if none
  published (document)
- **[Trade-off] Drop plexsystems Action** → Acceptable; pin becomes explicit

## Migration Plan

1. Land script + workflow + docs + allowlist
2. Archive/sync OpenSpec
3. Product sync picks up script + check workflow

## Open Questions

- None (A locked)
