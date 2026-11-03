## 1. Workflows

- [x] 1.1 In `reusable-check.yml` Licence Check and Security Check: checkout when `!skip`, read `TRIVY_VERSION` from
      `versions.env` (fail closed), pass `version:` on every `trivy-action` step — verify YAML parses / step ids align
- [x] 1.2 In `reusable-release.yml` Trivy license scan path: same read + `version:` wiring — verify release job still
      continues on license findings as today

## 2. Docs

- [x] 2.1 Update `docs/ci.md`: CI Trivy binary follows `versions.env` / Renovate, independent of Action SHA; note
      product local-check mirrors — verify Prettier/markdownlint

## 3. Validate

- [x] 3.1 Run `openspec validate trivy-version-ci --strict` — verify exit 0
