## 1. Dependency, baseline, runner

- [ ] 1.1 Add pinned `import-linter` to the shared uv quality dependency set; verify `uv run lint-imports --help` (or
      package entry) works after lock/sync
- [ ] 1.2 Add synced baseline `.importlinter` (`root_package = middleware`, `exclude_type_checking_imports = True`,
      `acyclic_siblings` for `middleware`) and verify the file parses / dry-runs without a product tree (or skips cleanly
      when `middleware/` is absent in Devinfra)
- [ ] 1.3 Add synced `scripts/run-import-linter.sh` that always applies the baseline and merges `.importlinter.product`
      when present; verify merge behavior with a fixture overlay in a dry run

## 2. Hooks, CI, sync allowlist

- [ ] 2.1 Wire commit-stage pre-commit to the runner and reusable code-quality to the same runner; verify YAML/hook
      entries match
- [ ] 2.2 Add baseline path to `docs/synced-paths.yaml` `allow` and `.importlinter.product` to `overlays`; update
      `docs/sync.md` / `docs/quality.md` accordingly and verify lint/format clean

## 3. Docs and code-review

- [ ] 3.1 Document parity (hooks+CI, IDE exception), Import-policy mapping (what is / isn’t gated), and pydeps non-gate
      in `docs/quality.md` + principles Code Quality example
- [ ] 3.2 Update `.agents/skills/code-review/SKILL.md` and `docs/code-review.md` so import-linter is toolchain-owned;
      verify judgment remains for non-linter Import-policy rules

## 4. Validate

- [ ] 4.1 Run `openspec validate fleet-import-linter-contracts --strict` and confirm pass
- [ ] 4.2 Comment on GitHub #173 with links to the three product overlay follow-up issues and verify the comment is
      visible
