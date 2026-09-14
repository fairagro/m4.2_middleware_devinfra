# Trivy license: report-only in check, section on GitHub Release — Proposal

## Why

Alpine-based product images fail `reusable-check` Licence Check on expected OS GPL licenses (Trivy `restricted`/HIGH),
blocking PR CI without a vulnerability finding. Operators still need a readable license inventory on the GitHub Release,
not a silent merge blocker.

## What Changes

- **BREAKING (policy):** Licence Check in `reusable-check.yml` MUST NOT fail the job on Trivy license findings
  (`exit-code: 0`); keep the dedicated job and table output; optionally upload a JSON report artifact. Vulnerability /
  SBOM scanning policy unchanged.
- When `reusable-release.yml` creates a GitHub Release, append a **readable license section** derived from a Trivy
  license scan of the released image(s) (re-scan in release; do not depend on check artifacts).
- Document in `docs/ci.md`: license = inform on release / non-blocking in check; vulns remain the gate.
- Keep job display name **Licence Check** for branch-ruleset stability.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `reusable-ci-workflows`: Check licence scan is report-only (must not fail CI); Docker release body includes a readable
  Trivy license summary when a GitHub Release is created

## Impact

- `.github/workflows/reusable-check.yml`, `.github/workflows/reusable-release.yml`, `docs/ci.md`
- Spec delta under `openspec/specs/reusable-ci-workflows/`
- Product callers (harvester / API / sql-to-arc) pick up on next workflow ref bump — no product-local forks
- Out of scope: relicensing Alpine, disabling vuln scans, SARIF upload for license (optional linked follow-up)
