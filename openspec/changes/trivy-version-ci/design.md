## Context

See proposal.md — Why. Fleet already pins `TRIVY_VERSION` in `versions.env` for the Dev Container; Renovate tracks it.
`trivy-action` @ SHA `ed142fd…` (v0.36.0) defaults to bundled Trivy `v0.70.0` when `version` is omitted. Locked scope:
**A+C** — wire pin in `reusable-check.yml` and `reusable-release.yml` (#329).

## Goals / Non-Goals

**Goals**

- CI Trivy binary tracks caller `versions.env` for all check + release Action invocations
- Fail closed on missing/empty pin; document independence from Action SHA

**Non-Goals**

- Bumping Action SHA or Renovate Action managers
- Editing product-vendored `reusable-check-local.yml` in this PR (sync after merge)
- Changing licence report-only or vuln CRITICAL/HIGH fail policy

## Decisions

1. **Checkout before read** — Licence Check and Security Check today have no checkout (artifact-only). Add
   `actions/checkout@v7` (same as CST) when `!skip`, then awk `TRIVY_VERSION` into a step output. Release license job:
   add checkout + same read if not already present before Trivy.
2. **Read pattern** — Copy UV_VERSION idiom from `reusable-code-quality.yml` / CodeQL: awk `^TRIVY_VERSION=`, trim,
   empty → exit 1 with named error; `echo "version=…" >> "$GITHUB_OUTPUT"`.
3. **Pass `version:`** — Every `aquasecurity/trivy-action` `with:` in those two workflows gets
   `version: ${{ steps.trivy-version.outputs.version }}` (or shared step id). Keep Action SHA pin unchanged.
4. **Docs** — Short subsection in `docs/ci.md` near existing Trivy licence/vuln prose.

## Risks / Trade-offs

- **[Risk] Extra checkout cost on matrix jobs** → Acceptable; matches CST; needed for SoT pin
- **[Risk] Pin format mismatch** → Fleet already uses `v0.74.0`-style; Action expects that form
- **[Trade-off] Local check mirrors lag until sync** → Document; do not block Devinfra merge

## Migration Plan

1. Land workflows + docs in Devinfra
2. Archive/sync OpenSpec requirement
3. Product sync / local-check mirrors pick up on next sync

## Open Questions

- None for MVP (A+C locked)
