## Why

CI Security/Licence checks (and release Trivy license scans) use SHA-pinned `aquasecurity/trivy-action` without a
`version:` input, so the Action installs its bundled default Trivy while fleet `versions.env` `TRIVY_VERSION` (Dev
Container / Renovate) never reaches those jobs. Bumping the pin alone does not move CI scans (#329).

## What Changes

- Read `TRIVY_VERSION` from the **caller** checkout’s `versions.env` in `reusable-check.yml` (Licence + Security) and
  `reusable-release.yml` (Trivy license scan for release body), fail closed if missing/empty
- Pass `version:` into every `aquasecurity/trivy-action` invocation in those workflows
- Document in `docs/ci.md` that the CI Trivy binary follows `versions.env` / Renovate, independent of the Action SHA pin
- Product `reusable-check-local.yml` mirrors remain a post-merge sync concern (out of Devinfra MVP code)

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `reusable-ci-workflows`: CI Trivy binary MUST come from caller `versions.env` `TRIVY_VERSION` for check and release
  Trivy Action steps

## Impact

- `.github/workflows/reusable-check.yml`, `.github/workflows/reusable-release.yml`, `docs/ci.md`
- OpenSpec `reusable-ci-workflows` main spec (on archive)
- Callers that vendor a local check workflow must mirror when syncing
