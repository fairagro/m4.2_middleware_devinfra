## ADDED Requirements

### Requirement: Shared Renovate opens vulnerability fix PRs

The shared `renovate.json` MUST enable Renovate `vulnerabilityAlerts` so that, when GitHub Dependabot vulnerability
alerts are present and a fix version is available for a managed dependency, Renovate opens a remediation pull request.
It MUST enable `osvVulnerabilityAlerts` so Renovate also opens remediation pull requests for known OSV vulnerabilities
on **direct** dependencies using Renovate-supported datasources (at least those Renovate documents for OSV, including
`npm` and `pypi`). Vulnerability remediation PRs MUST carry a `security` label (in addition to the shared default
dependency labels when applicable) and MUST use a schedule of `at any time` so they are not deferred to maintenance
windows. Existing repository PR rate limits (`prHourlyLimit` / `prConcurrentLimit`) MAY still apply. This requirement
MUST NOT claim that Renovate consumes GitHub Code Scanning alerts (including Trivy SARIF).

#### Scenario: Dependabot alert can become a Renovate PR

- **WHEN** a repository using the shared config has an open Dependabot vulnerability alert for a Renovate-managed
  dependency with an available fix version
- **AND** Renovate runs successfully with a token that can read vulnerability alerts
- **THEN** Renovate opens (or updates) a remediation pull request for that dependency
- **AND** the PR is labeled `security`

#### Scenario: OSV direct-dependency vulnerability can become a Renovate PR

- **WHEN** a direct dependency managed by a supported OSV datasource has a known vulnerability with an available fix
- **AND** Renovate runs successfully
- **THEN** Renovate opens (or updates) a remediation pull request
- **AND** the PR is labeled `security`

#### Scenario: Code Scanning / Trivy stays out of Renovate vulnerability alerts

- **WHEN** a maintainer reads the shared Renovate vulnerability configuration or docs after this change
- **THEN** they learn vulnerability fix PRs come from Dependabot alerts and/or OSV
- **AND** they learn Trivy Code Scanning findings are not inputs to these Renovate knobs

## MODIFIED Requirements

### Requirement: Renovate documentation covers token, dry-run, and Dependabot migration

The repository MUST document: (1) creating `DEVINFRA_BOT_TOKEN` as a GitHub Actions repository secret (fine-grained PAT
or equivalent scopes for contents/PRs as required by Renovate and product sync — not SOPS-in-repo), including that the
token MUST be able to read GitHub Dependabot vulnerability alerts when `vulnerabilityAlerts` is enabled; (2) local CLI
dry-run using the Dev Container pinned `renovate` against the shared config; (3) product migration — remove Dependabot
**version update** config (`dependabot.yml`); keep Dependabot **alerts**; prefer Renovate for dependency update PRs
(avoid dual general updaters); turn off Dependabot **security update** PRs when Renovate owns vulnerability remediation
so only one bot opens fix PRs; (4) sync/adoption via #13 for API / sql-to-arc / harvester; (5) that shared Renovate
enables `vulnerabilityAlerts` and `osvVulnerabilityAlerts`, with OSV limited to direct dependencies on supported
datasources, and that neither knob consumes Trivy / Code Scanning SARIF. The root README Docs index (or CI/Dev Container
docs) MUST link to this documentation.

#### Scenario: Operator prepares Renovate on a new repo

- **WHEN** an operator follows the Renovate docs to enable automation
- **THEN** they learn to set repository secret `DEVINFRA_BOT_TOKEN` in GitHub Actions settings
- **AND** they find a local dry-run command using the pinned CLI
- **AND** they learn to remove Dependabot version updates while keeping alerts
- **AND** they learn to prefer Renovate over Dependabot security-update PRs for vulnerability fixes
- **AND** they learn vulnerability fix PRs use Dependabot alerts and OSV, not Trivy Code Scanning
