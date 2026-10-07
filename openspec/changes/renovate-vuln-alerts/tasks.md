## 1. Config

- [ ] 1.1 Enable `osvVulnerabilityAlerts` and configure `vulnerabilityAlerts` (`enabled`, `security` label,
      `schedule: at any time`) in root `renovate.json` — verify JSON still validates against the Renovate schema /
      `renovate config` dry-run if available
- [ ] 1.2 Confirm vulnerability policy does not disable existing managers or product SoT `packageRules` — verify
      `enabledManagers` and product-disable rules unchanged in intent

## 2. Docs

- [ ] 2.1 Update `docs/renovate.md` Dependabot migration / security section for both knobs, token alert-read
      requirement, Prefer Renovate over Dependabot security-update PRs, OSV limits, vs Trivy Code Scanning — verify
      Prettier / markdownlint on touched docs

## 3. Validate

- [ ] 3.1 Ensure delta `shared-renovate` matches shipped config/docs — verify
      `openspec validate renovate-vuln-alerts --strict`
