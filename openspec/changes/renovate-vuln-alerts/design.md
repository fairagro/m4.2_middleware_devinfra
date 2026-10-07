## Context

See proposal.md — Why. Lock-in for this change is **B**: enable both alert sources and apply a security-oriented PR
policy (label + immediate schedule). Shared config already uses `extends: ["config:recommended"]`, default
`labels: ["dependencies"]`, and PR rate limits.

## Goals / Non-Goals

**Goals:**

- Dependabot alert → Renovate fix PR when a managed fix version exists.
- OSV → Renovate fix PR for eligible direct dependencies.
- Vulnerability PRs labeled `security` and scheduled `at any time`.
- Docs/spec parity with GitHub prerequisites and Trivy non-goals.

**Non-Goals:**

- Bridging Trivy / Code Scanning SARIF into Renovate.
- Automerge of security PRs.
- Changing `prHourlyLimit` / `prConcurrentLimit`.
- Expanding OSV beyond what Renovate supports (no custom transitive scanner).

## Decisions

1. **Both knobs on** — `vulnerabilityAlerts` (GitHub) and `osvVulnerabilityAlerts` (OSV). Meets #296 AC; accepts some
   duplicate-PR risk for the same direct dep.
2. **Policy via `vulnerabilityAlerts` object** — Renovate merges this object into vulnerability remediation PRs (same
   family as packageRules). Set `enabled: true`, `labels: ["security"]` (shared default `dependencies` still applies
   unless Renovate replaces; document expected labels), `schedule: ["at any time"]`. Prefer this over a separate
   `packageRules` matcher so OSV and Dependabot-sourced vuln PRs share one policy surface.
3. **`osvVulnerabilityAlerts: true`** as top-level boolean (Renovate schema).
4. **Docs harden Dependabot security-update PRs off** — already optional; make it the recommended product posture when
   Renovate owns fixes.
5. **Token** — document that `DEVINFRA_BOT_TOKEN` needs permission to read Dependabot vulnerability alerts; do not
   invent a second secret name.

**Alternatives considered:** A (enable without schedule/label policy) — deferred; C/D (single source) — reject vs AC.

## Risks / Trade-offs

- **[Risk]** Duplicate PRs (Dependabot security updates + Renovate, or OSV + Dependabot for same direct dep) →
  Mitigation: docs: disable Dependabot security-update PRs; operators close duplicates; rate limits bound burst.
- **[Risk]** Token cannot read alerts → Mitigation: docs list required capability; Renovate logs make failures visible.
- **[Trade-off]** OSV skips most transitives → Accept; lockfile maintenance / normal updates remain the broader path;
  Dependabot alerts still cover many lockfile CVEs for `vulnerabilityAlerts`.
- **[Trade-off]** `security` label may be missing on a fresh product repo → Renovate typically creates labels when
  permitted; docs note the label name.

## Migration Plan

1. Land `renovate.json` + docs + delta on Devinfra `main`.
2. Sync to products; confirm Dependabot alerts on / security-update PRs off.
3. Next Renovate run may open PRs for existing open alerts (e.g. Devinfra Dependabot queue).
