## 1. Dependency, baseline, runner

- [x] 1.1 Add pinned `import-linter` to the shared uv quality dependency set; verify `uv run lint-imports --help` (or
      package entry) works after lock/sync
- [x] 1.2 Add synced baseline `.importlinter.global` (`root_package = middleware`, `exclude_type_checking_imports =
      True`, `acyclic_siblings` for `middleware`) and verify skip when `middleware/` is absent in Devinfra
- [x] 1.3 Add synced `scripts/run-import-linter.sh` that always applies `.importlinter.global` and merges `.importlinter`
      when present; verify merge behavior with a fixture overlay in a dry run

## 2. Hooks, CI, sync allowlist

- [x] 2.1 Wire commit-stage pre-commit to the runner and reusable code-quality to the same runner; verify YAML/hook
      entries match
- [x] 2.2 Add `.importlinter.global` to `docs/synced-paths.yaml` `allow` and `.importlinter` to `overlays`; update
      `docs/sync.md` / `docs/quality.md` / principles naming rule accordingly and verify lint/format clean

## 3. Docs and code-review

- [x] 3.1 Document parity (hooks+CI, IDE exception), Import-policy mapping (what is / isn’t gated), and pydeps non-gate
      in `docs/quality.md` + principles Code Quality example
- [x] 3.2 Update `.agents/skills/code-review/SKILL.md` and `docs/code-review.md` so import-linter is toolchain-owned;
      verify judgment remains for non-linter Import-policy rules

## 4. Validate

- [x] 4.1 Run `openspec validate fleet-import-linter-contracts --strict` and confirm pass
- [x] 4.2 Comment on GitHub #173 with links to the three product overlay follow-up issues and verify the comment is
      visible
