## Why

Dependabot alerts already surface lockfile/manifest CVEs on GitHub, but shared Renovate does not open targeted fix PRs
from those alerts or from OSV. Routine version bumps and Monday lockfile maintenance are too slow/noisy as the only
remediation path. Trivy Code Scanning remains a separate surface (out of scope).

## What Changes

- Enable `vulnerabilityAlerts` and `osvVulnerabilityAlerts` in shared `renovate.json`.
- Apply security-oriented PR policy on vulnerability fix PRs (lock-in **B**): label(s) including `security`, schedule
  `at any time` (not bound to maintenance windows), within existing PR rate limits.
- Document both knobs, GitHub prerequisites (Dependency graph + Dependabot alerts), Prefer Renovate over Dependabot
  **security update** PRs, limits (OSV = direct deps / listed datasources), and distinction from Trivy Code Scanning.
- Extend `shared-renovate` OpenSpec accordingly.

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `shared-renovate`: Vulnerability fix PRs from Dependabot alerts + OSV, with security PR policy; docs cover both knobs
  vs Trivy / Dependabot security updates.

## Impact

- Devinfra: `renovate.json`, `docs/renovate.md`, `openspec/specs/shared-renovate` (via archive sync).
- Products: pick up config on sync; operators should keep Dependabot alerts on and turn off Dependabot security-update
  PRs if Renovate owns fixes; `DEVINFRA_BOT_TOKEN` must be able to read vulnerability alerts.
- No Trivy / `reusable-check` SARIF changes.
