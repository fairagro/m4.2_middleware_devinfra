# Shared Renovate config + workflow (issue #38)

## Why

Devinfra pins the Renovate CLI and mentions local dry-runs, but has no canonical `renovate.json` or GitHub Renovate
workflow. Product repos diverge (API already on Renovate; sql-to-arc / harvester still on Dependabot version updates).
We need one shared Renovate surface here so sync (#13) can converge products: everything Renovate can update should be
Renovate.

## What Changes

- Add Devinfra `renovate.json` seeded from the API config, extended for Devinfra `versions.env` / toolchain pins
  (explore **A1**). Treat as shared SoT; products may later `extends` or sync a copy with thin overlays via #13.
- Add per-repo `.github/workflows/renovate.yml` (schedule + `workflow_dispatch` + push on config; self-hosted
  `renovatebot/github-action` + `RENOVATE_TOKEN`) — same shape as API (**B1**). No `reusable-renovate.yml` in this
  change.
- Document: `RENOVATE_TOKEN` as a GitHub Actions repo secret (not SOPS); local CLI dry-run against the pinned version;
  Dependabot migration — keep alerts, remove version-update `dependabot.yml`, prefer Renovate for update PRs (**C1**,
  **E1**).
- Docs clear sync/adoption path for the three product repos (#13); Devinfra-only implementation in this PR (**D1**).
- Add Renovate paths to the synced-paths allowlist so consumers do not hand-edit after sync.

## Capabilities

### New Capabilities

- `shared-renovate`: Canonical Renovate config, GitHub workflow, and docs for Devinfra and synced product consumers
  (token, dry-run, Dependabot migration).

### Modified Capabilities

- `shared-devcontainer-base`: Local Renovate CLI docs MUST point at the shared config/workflow (no longer “workflow
  deferred to open issues only”).
- `synced-consumer-paths`: Allowlist MUST include `renovate.json` and `.github/workflows/renovate.yml` (when sync ships
  them).

## Impact

- New: `renovate.json`, `.github/workflows/renovate.yml`, docs (`docs/renovate.md` and/or `docs/ci.md` /
  `docs/devcontainer.md` / README)
- `docs/synced-paths.global.md`
- OpenSpec specs above; product cutover remains #13 / product PRs (not this repo)
- Ops: create `RENOVATE_TOKEN` Actions secret on Devinfra (and later on each product) — outside git
