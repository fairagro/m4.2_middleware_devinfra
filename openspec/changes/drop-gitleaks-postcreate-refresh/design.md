## Context

See `proposal.md`. Image already installs gitleaks; postCreate soft-refresh is the last CLI exception after #383 docs
lock-in (rebuild for new hooks).

## Goals / Non-Goals

**Goals:**

- Remove postCreate gitleaks refresh; Spec + docs match actionlint rebuild bar
- Forbid shared postCreate from refreshing pinned CLIs via `install-pinned-tool.sh`

**Non-Goals:**

- Dockerfile → `install-pinned-tool.sh` (#374)
- Changing CI install steps for gitleaks/actionlint

## Decisions

1. **Delete the block** — no shim, no flag; soft-WARNING path goes away.
2. **Rename scenario** — `Contributor has gitleaks after Dev Container create` → `… after Dev Container rebuild`
   (parallel to actionlint).
3. **postCreate MUST NOT** — explicit in `shared-devcontainer-base` so the exception cannot creep back via docs-only.

## Risks / Trade-offs

- [Stale binary until rebuild] → Same as actionlint; documented in #383/#384.
- [Hosts without image] → Host path remains `install-pinned-tool.sh`; out of Dev Container happy path.

## Migration Plan

1. Land script + docs + delta on Devinfra; sync carries postCreate to products.
2. No dual-run; next create after sync skips gitleaks download.

## Open Questions

None.
