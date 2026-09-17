## ADDED Requirements

### Requirement: Complementary concurrency on outer reusable workflows

The repository’s outer `workflow_call` reusables used directly by product callers — at least
`reusable-code-quality.yml`, `reusable-build.yml`, `reusable-check.yml`, `reusable-release.yml`,
`reusable-helm-release.yml`, `reusable-helm-pre-release.yml`, and `reusable-registry-retry.yml` — MUST declare a
workflow-level `concurrency` group that includes the caller `github.repository`, a stable reusable identity (e.g.
workflow file name), and the pull request number when present otherwise the git ref. Feature-oriented reusables
(code-quality, build, check) MUST set `cancel-in-progress: true`. Publish-oriented reusables (Docker release, Helm
final/pre-release, registry-retry) MUST set `cancel-in-progress: false` so overlapping runs of the same reusable for the
same repository+ref serialize instead of aborting a half-finished publish.

This complementary concurrency MUST NOT be documented or treated as a substitute for caller-level concurrency that
cancels an entire product Feature-PR pipeline. Nested helper reusables invoked only from other Devinfra reusables (e.g.
Bake / registry push / Helm OCI push) MAY omit their own concurrency in this change.

#### Scenario: Feature-oriented reusable cancels duplicate runs

- **WHEN** two concurrent calls of the same outer feature-oriented reusable target the same repository and the same PR
  number (or ref)
- **THEN** the reusable’s concurrency group cancels the in-progress run (`cancel-in-progress: true`)

#### Scenario: Publish-oriented reusable serializes without cancel

- **WHEN** two concurrent calls of the same outer publish-oriented reusable target the same repository and ref
- **THEN** the reusable’s concurrency group serializes them with `cancel-in-progress: false`

### Requirement: Feature-PR and release concurrency caller documentation

Documentation in this repository (at least `docs/ci.md`) MUST provide a **complete recommended Feature-PR caller**
snippet that includes: (1) workflow-level `concurrency` grouped by PR number (or equivalent) with
`cancel-in-progress: true`; (2) a full `detect-changes` job using a paths-filter action with a **suggested default**
path set for a `code` (or equivalent) output, plus a note that products may extend the filter (e.g. `stubs/`,
`docker-bake.hcl`, `versions.env`); (3) wiring `skip` from that output into reusable code-quality / build / check, and
the check job `if:` / build-result combination consistent with the existing skip contract. Documentation MUST also guide
**release / pre-release / Helm** callers to prefer a concurrency group that serializes overlapping runs of the same
workflow+ref with `cancel-in-progress: false`, and MUST state that `detect-changes` / `skip` is Feature-PR-oriented and
not required for dispatch release callers. Documentation MUST state explicitly that reusable-level concurrency does not
replace caller-level cancel for the full PR pipeline, and that `skip` remains a **caller** responsibility
(`detect-changes` stays product-local).

#### Scenario: Contributor copies Feature-PR concurrency and detect-changes

- **WHEN** a product maintainer reads the Feature-PR section of the CI docs after this change
- **THEN** they see workflow-level cancel-in-progress concurrency
- **AND** they see a full `detect-changes` job with a suggested path filter and `skip` wiring into quality/build/check
- **AND** they learn reusable concurrency does not replace that caller-level cancel

#### Scenario: Contributor configures release concurrency

- **WHEN** a product maintainer reads the release / Helm caller guidance after this change
- **THEN** they learn to serialize with `cancel-in-progress: false`
- **AND** they learn `detect-changes` is not required for those dispatch callers
