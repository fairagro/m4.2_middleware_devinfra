## Context

See proposal.md — Why. Explore lock-in: report-only Licence Check (`exit-code: 0`); keep job name; re-scan in
`reusable-release` for the release-body section; document in `docs/ci.md`; OpenSpec delta on `reusable-ci-workflows`.
Vuln/SARIF path unchanged. Optional SARIF-for-license is a linked follow-up, not MVP.

## Goals / Non-Goals

**Goals:**

- Alpine product-app images pass PR check despite base GPL/`restricted` license hits
- GitHub Release body shows a readable license inventory per component
- Specs and `docs/ci.md` state the policy clearly

**Non-Goals:**

- Relicensing products or banning Alpine
- Changing vulnerability fail policy
- Depending on check artifacts for release (check may be skipped)
- Uploading license SARIF to code scanning (follow-up)

## Decisions

1. **`exit-code: "0"` on licence scanner in check**
   - **Why:** Minimal change; keeps table output and job name for rulesets.
   - **Alt:** Drop job / ignore severities — rejected; operators want visibility in CI logs.
2. **Optional JSON artifact from check**
   - Upload Trivy JSON for debugging; not required by release.
3. **Re-scan in release before/while generating `release-body.md`**
   - Load `docker-image-<component>` artifact (already available in release path), run Trivy license (JSON or table →
     Markdown), append section. Works when check was skipped.
   - **Alt:** Consume check artifact — rejected for skip/ordering fragility.
4. **Markdown shape:** counts + compact table; truncate with “see workflow log” if over a fixed row budget.
5. **Format only touched docs** (no repo-wide Prettier drive-by).

## Risks / Trade-offs

- **[Risk] Release job slower / needs Trivy action pin** → Mitigation: same pinned `trivy-action` digest as check;
  matrix already per-component for pushes — license step on github-release job may loop components once.
- **[Risk] Huge Alpine license lists** → Mitigation: truncate + log pointer.
- **[Risk] Callers pin old `@sha` of reusable-check** → Mitigation: docs note BREAKING policy; products bump ref (Wave C
  / sync).

## Migration Plan

1. Merge Devinfra PR; products bump `uses:` ref.
2. No product-local workflow forks for this policy.
3. Rollback = revert Devinfra commit / pin prior ref.
