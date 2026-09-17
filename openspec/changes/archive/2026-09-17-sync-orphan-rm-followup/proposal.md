## Why

Sync is still add/update-only: allowlist drops and Devinfra deletions leave orphaned files in products, and
product-local cleanup after contract changes (e.g. stubs removal) depends on someone remembering to open follow-up
issues. Discussion [#166](https://github.com/fairagro/m4.2_middleware_devinfra/issues/166) locked deletes via allowlist
delta plus explicit `SYNC-FOLLOWUP` product issues; this change implements that contract with plumbing in `m42-ai`.

## What Changes

- **BREAKING (sync contract):** Sync PRs MAY `git rm` product paths that disappear from the resolved allowlist file set
  between the workflow `before` SHA and `HEAD` (delta orphan removal). No `retire:` list.
- On live sync / dispatch: parse `SYNC-FOLLOWUP: <stable-id>` from the merged Devinfra PR **body and comments**; open
  one deduped Task issue per product repo (manual `workflow_dispatch` input uses the same id).
- Prefer new/extended **`m42-ai`** commands for PR-for-SHA, trailer parse, and issue ensure/dedupe; thin
  `sync-products.py` + workflow orchestration.
- Update `docs/sync.md` (and bot permission notes if needed) for delete semantics, trailer, and dispatch input.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `product-repo-sync`: Replace v1 “MUST NOT delete” with delta orphan `git rm`; document/require `SYNC-FOLLOWUP`
  handling and dispatch follow-up input; docs MUST describe the new contract.
- `agent-ai-gh`: CLI MUST support sync-followup plumbing (resolve PR for commit, parse trailers from body/comments,
  ensure deduped product follow-up issues) callable from sync orchestration.

## Impact

- `scripts/sync-products.py`, `.github/workflows/sync-products.yml` (Devinfra-only)
- `scripts/ai` (`m42-ai` + tests)
- `docs/sync.md`, possibly `docs/renovate.md` (Issues write already listed for the bot)
- `openspec/specs/product-repo-sync`, `openspec/specs/agent-ai-gh`
- Product sync PRs may contain deletions; older orphans from before this lands stay until a later delta or manual
  `SYNC-FOLLOWUP`
