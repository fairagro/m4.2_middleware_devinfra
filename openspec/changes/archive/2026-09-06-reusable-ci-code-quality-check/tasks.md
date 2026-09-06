# Reusable CI code-quality + check — Tasks

## 1. Workflows

- [x] 1.1 Add `.github/workflows/reusable-code-quality.yml` adapted from the API product: `workflow_call` inputs include
      `skip`, `python_package_root` (default `middleware`), and keep unused-but-compatible `components` if callers
      already pass it; job name `Code Quality Check (3.12)`; versions.env assert + load; ruff/pylint/mypy/bandit/pytest
      against the package-root input; Bandit medium/high fail policy
- [x] 1.2 Add `.github/workflows/reusable-check.yml` adapted from the API product: inputs `version`, `components`,
      `skip`, `image_base_name`; licence + Trivy image/SBOM SARIF + CST jobs; documented artifact names; CST config
      under `docker/container-structure-tests/<component>.yaml`; skip no-op paths for required statuses

## 2. Documentation

- [x] 2.1 Add `docs/ci.md` covering `uses: …@ref` (main vs tag/SHA), inputs, check artifact contract, and that
      build/release reusables are out of MVP
- [x] 2.2 Add a short README pointer to `docs/ci.md`

## 3. Verify

- [x] 3.1 Sanity-check YAML structure (parse / actionlint if available in the environment)
- [x] 3.2 Format/lint touched Markdown (`npm run format:md` / `lint:md` as needed)
