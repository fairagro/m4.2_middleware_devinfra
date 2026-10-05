## 1. Reusable workflow

- [ ] 1.1 Add `.github/workflows/reusable-helm-lint.yml` with `chart_dir`, `skip`, `run_template` (default true), Helm
      pin from caller `versions.env`, `helm lint`, optional `helm template`, and skip no-op — verify YAML parses
      (`actionlint` if available, or visual review against code-quality skip pattern)
- [ ] 1.2 Confirm concurrency / permissions match feature-oriented reusables (`contents: read`, cancel-in-progress true)
      — verify group naming parallels `reusable-code-quality.yml`

## 2. Documentation

- [ ] 2.1 Update `docs/ci.md` Feature-PR section: table row for the new reusable; separate chart detect-changes output +
      lint job example; explicit warning not to use Docker `code` alone — verify `npm run lint:md` / format check on
      touched docs when run locally
- [ ] 2.2 Add a short inputs subsection for `reusable-helm-lint.yml` (mirror other reusable input tables) — verify
      `chart_dir` / `skip` / `run_template` documented

## 3. Spec sync readiness

- [ ] 3.1 Ensure delta specs under `openspec/changes/reusable-helm-lint/specs/` match the shipped workflow and docs —
      verify `openspec validate reusable-helm-lint --strict` (or project equivalent) passes
