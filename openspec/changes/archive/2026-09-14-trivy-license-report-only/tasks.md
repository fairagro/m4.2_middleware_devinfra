## 1. Check: license report-only

- [x] 1.1 Set Licence Check Trivy `exit-code` to `0` (keep scanners/license, severity, table, job name)
- [x] 1.2 Optionally upload a JSON license report artifact per component for debugging

## 2. Release: license section in body

- [x] 2.1 In `reusable-release` (when creating a GitHub Release), load each component image and run Trivy license scan
- [x] 2.2 Append a readable Markdown license section (counts + package/license/classification; truncate if needed)
- [x] 2.3 Ensure license findings do not fail the release solely on classification hits

## 3. Docs and validate

- [x] 3.1 Document policy in `docs/ci.md` (license inform / non-blocking; vulns remain gate)
- [x] 3.2 Format only touched Markdown; `openspec validate trivy-license-report-only --strict`
