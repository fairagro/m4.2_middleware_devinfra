## Context

See `proposal.md`. Push currently always appends `--skip-infrastructure`; dispatch input defaults to `true`.

## Goals / Non-Goals

**Goals:**

- Include Infra on push and dispatch by default
- Keep `skip_infrastructure` for ops emergencies (dispatch)

**Non-Goals:**

- Changing Infra profile allowlist / Dev Container adoption
- Enabling Infra `SYNC-FOLLOWUP` ensure
- Commenting on infra#80 (post-merge operator note)

## Decisions

1. **Remove push hard-skip** — do not pass `--skip-infrastructure` on push.
2. **Dispatch default false** — operators set `skip_infrastructure=true` only when needed; dry-run still defaults
   `dry_run=true`.
3. **No new push skip input** — emergency omit on push is a temporary workflow edit or wait for dispatch-only sync.

## Risks / Trade-offs

- [Unexpected Infra sync PRs on next allowlist push] → Intended; Slice-2 checklist done.
- [Ops wants push-time skip without editing YAML] → Accepted; use dispatch with skip or revert PR.

## Migration Plan

1. Land workflow + docs + specs.
2. After merge, confirm next allowlist-touching `main` push (or one live dispatch) syncs Infra.
3. Brief note on infra#80 (operator).

## Open Questions

None.
