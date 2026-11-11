## 1. Fragments and compose

- [ ] 1.1 Add profile fragments for foundation / python-product / gitops from the locked hook map; add compose script
      that writes root `.pre-commit-config.yaml`; regenerate Devinfra root and verify product-union hook ids match prior
      behavior (incl. helm-lint + pre-push)
- [ ] 1.2 Document fragment paths, compose command, consumer matrix (products vs Infra), and migration in
      `docs/quality.md` (and sync cross-links as needed); verify docs do not tell consumers to hand-edit only the root

## 2. Sync profiles and Infra wiring

- [ ] 2.1 Update `docs/synced-paths.yaml` with a `gitops` profile, fragment/compose allow entries, and target profile
      lists (products: foundation+python-product+gitops; infrastructure: foundation+gitops); adjust `docs/sync.md` /
      README inventory; verify `--list-files --target` differs (Infra lacks python-product hooks)
- [ ] 2.2 Remove obsolete “Wave A” / “Wave-A” wording from live SoT touched by this change (`README.md`,
      `openspec/specs/product-repo-sync` after apply sync, and any other live docs edited here); verify grep on those
      paths is clean (archives untouched)

## 3. Tests and validate

- [ ] 3.1 Add/extend tests for compose determinism and profile allow resolution (missing python-product on Infra);
      verify `uv run pytest` on touched modules
- [ ] 3.2 Run `openspec validate pre-commit-profile-hooks --strict` and Prettier/markdownlint on touched Markdown;
      verify clean
