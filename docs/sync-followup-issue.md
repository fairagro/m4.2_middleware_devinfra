# Sync follow-up issue template (Devinfra-only — not on the product sync allowlist)

## Type

Task

## Triage

- **severity:** low
- **practicality:** n/a (no defect path)
- **cost:** medium (override via CLI if needed)

## Problem

Devinfra sync requested product-local follow-up work for stable id `{stable_id}`.

After merging the corresponding Devinfra sync PR, complete any cleanup that copy/`git rm` did not cover (product-only
paths, CI env, call-site ignores, docs).

## Acceptance criteria (suggested)

- [ ] Address the follow-up described in the linked Devinfra PR
- [ ] Do not hand-edit synced allowlist paths — land shared fixes in Devinfra
- [ ] Commit-stage hooks / code-quality CI stay green

## Links

- Source PR: {source_pr_url}
- Source SHA: `{source_sha}`
