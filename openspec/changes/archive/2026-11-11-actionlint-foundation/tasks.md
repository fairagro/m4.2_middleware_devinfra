## 1. Pin + install + image

- [x] 1.1 Add `ACTIONLINT_VERSION` to `versions.env` and a Renovate customManager entry (gitleaks pattern) — verify
      Renovate matchString would capture the pin
- [x] 1.2 Add `scripts/install-actionlint.sh` (fail closed without pin; install to PATH) — verify
      `bash scripts/install-actionlint.sh` installs the pinned binary in Dev Container
- [x] 1.3 Wire Dockerfile `ARG`/`RUN` + compose build-arg for actionlint — verify image rebuild docs mention the pin
- [x] 1.4 Allowlist `scripts/install-actionlint.sh` under `foundation` in `docs/synced-paths.yaml` — verify profile
      tests still pass

## 2. Hooks + CI

- [x] 2.1 Add foundation `actionlint` local hooks to `.pre-commit-config.yaml` and
      `.pre-commit-config.infrastructure.yaml` (files under `.github/workflows/`) — verify both configs list the hook
- [x] 2.2 Add blocking install + actionlint steps to `reusable-code-quality.yml` using the same pin — verify workflow
      YAML references `install-actionlint.sh` and fails closed on findings
- [x] 2.3 Run actionlint against this repo’s workflows (fix or document) — verify `actionlint` exits 0 on
      `.github/workflows` after any needed fixes

## 3. Docs + Infra note

- [x] 3.1 Document pin/hook/CI in `docs/quality.md`, `docs/ci.md`, and `docs/devcontainer.md` — verify markdownlint
      passes
- [x] 3.2 Comment on infra#80 with adoption path (hook via Infra root; pin via #354) — verify comment URL exists
- [x] 3.3 `openspec validate actionlint-foundation --strict` + Prettier on touched Markdown — verify validate succeeds
