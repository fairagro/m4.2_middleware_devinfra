## 1. Dual pre-commit configs

- [x] 1.1 Keep product `.pre-commit-config.yaml`; add hand-maintained `.pre-commit-config.infrastructure.yaml`
      (foundation + gitops hooks only); no compose script / `.pre-commit.d/`
- [x] 1.2 Document the two files, duplication trade-off, and Infra install in `docs/quality.md` (+ sync cross-links)

## 2. Sync profiles and Infra wiring

- [x] 2.1 Update `docs/synced-paths.yaml` (`gitops` profile for helm runner; Infra root on foundation; product root on
      python-product; targets foundation+python-product+gitops vs foundation+gitops); adjust `docs/sync.md` / README
- [x] 2.2 Remove obsolete lettered “wave” adopt labels from live SoT (`README.md`, `openspec/specs/product-repo-sync`,
      docs touched here); archives untouched

## 3. Tests and validate

- [x] 3.1 Tests for profile allow resolution (Infra lacks product pre-commit root / python-product hooks); verify pytest
- [x] 3.2 `openspec validate pre-commit-profile-hooks --strict` + Prettier/markdownlint on touched Markdown
