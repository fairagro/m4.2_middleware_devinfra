# Tasks: quality tools environment parity

## 1. Principles and docs

- [ ] 1.1 Add Code Quality subsection in `openspec/principles.global.md` for three-environment parity + minimal CLI
- [ ] 1.2 Document the same rule in `docs/quality.md` (IDE / hooks / CI table or short section; note IDE exceptions per
      design D4 if needed)
- [ ] 1.3 Cross-link from README quality blurb if it already summarizes gates

## 2. Audit and align invocations

- [ ] 2.1 Audit `.pre-commit-config.yaml`, `scripts/quality-check.sh`, `.github/workflows/reusable-code-quality.yml`,
      and `.vscode/settings.json` for config-file pointers and extra policy CLI flags
- [ ] 2.2 Remove or relocate any policy-on-CLI flags that belong in shared config files; keep only config path, targets,
      and documented path overlays
- [ ] 2.3 For tools without IDE integration, document “hooks + CI only” under the parity section (do not invent a second
      config)

## 3. Validate

- [ ] 3.1 Run Markdown format/lint on touched docs
- [ ] 3.2 Confirm `openspec validate quality-tools-env-parity --strict` (or project equivalent) passes
