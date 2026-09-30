## ADDED Requirements

### Requirement: Post-merge main Docker check caller for Code Scanning

Documentation in this repository (at least `docs/ci.md`) MUST provide a **complete recommended thin product caller** for
refreshing GitHub Code Scanning on the **default branch** after merge:

1. Trigger on `push` to `main` (or the repo default branch name when documented as such).
2. Call `reusable-build.yml` then `reusable-check.yml` only (same artifact contract as Feature PR Docker check) — MUST
   NOT include reusable code-quality or reusable Docker/Helm release / registry publish in this recommended snippet.
3. Grant top-level permissions that allow SARIF upload (`security-events: write`) and pass the usual product inputs
   (`components`, `image_base_name`, `version` from build outputs, `secrets: inherit` as needed).
4. Recommend caller-level concurrency for the workflow+ref (cancel-in-progress MAY be true) so overlapping main pushes
   do not pile up unbounded.

Documentation MUST state that this path exists so Default-Branch Trivy/Code Scanning alerts can auto-close when a clean
SARIF is uploaded for `main`, because Feature PR and Pre Release analyses are not attributed as default-branch closures.
Documentation MUST state that **Release keeps its own** `reusable-check` security gate and MUST NOT be documented as
consuming SARIF from this main-push run. Path filters MAY be mentioned as an optional later optimization and MUST NOT be
required for the v1 recommended snippet.

#### Scenario: Maintainer reads post-merge main check guidance

- **WHEN** a product maintainer opens `docs/ci.md` for post-merge / default-branch Trivy or Code Scanning alert hygiene
- **THEN** they find a complete thin caller snippet with `push` to `main`, `reusable-build`, and `reusable-check`
- **AND** the snippet does not add code-quality or Release/publish jobs
- **AND** they learn `security-events: write` is required for SARIF upload
- **AND** they learn Release still runs its own check and does not rely on this SARIF

#### Scenario: Feature PR template remains PR-oriented

- **WHEN** a contributor reads the recommended Feature PR caller after this change
- **THEN** Feature PR remains the `pull_request` quality/build/check path
- **AND** post-merge default-branch SARIF refresh is documented as a separate thin caller (not by requiring Feature PR
  to add `push: main` with the full job set)
