## 1. Cliff changelog template + helper

- [ ] 1.1 Add a usable `[changelog] body` template to `cliff.toml` (grouped Features / Bug Fixes / Breaking / … for
      GitHub markdown) — verify `git cliff` renders non-empty markdown on a sample range with conventional commits
- [ ] 1.2 Add `scripts/generate-release-changelog.sh` (`--surface docker|helm`) that resolves R1 previous tag, runs
      git-cliff with shared config, prints `## Changelog` markdown + optional compare link, soft-fails with placeholder
      on empty, logs clearly on cliff non-zero — verify docker vs helm tag globs and empty-range placeholder on a temp
      repo
- [ ] 1.3 Allowlist the new helper in `docs/synced-paths.yaml` (and sync.md inventory if required) — verify path appears
      under `allow`

## 2. Wire Final Release workflows

- [ ] 2.1 In `reusable-release.yml`: ensure git-cliff installed, call helper when building `release-body.md`, insert
      Changelog section, set `generate_release_notes: false` — verify workflow YAML references helper and flag
- [ ] 2.2 In `reusable-helm-release.yml`: same Changelog insert + `generate_release_notes: false` — verify YAML
- [ ] 2.3 Update `docs/ci.md` for Changelog section, R1 ranges, soft-fail, disabled GitHub auto-notes, compare link —
      verify docs mention Final-only (not pre-release)

## 3. Optional component scope in editor guidance

- [ ] 3.1 Update `.cursorrules` and `.vscode/settings.json` Copilot commit-message instructions to prefer
      `type(scope): subject` with a short component/area when clear from the full staged diff, without requiring scope —
      verify both files mention optional scope and do not imply `scope-enum`
- [ ] 3.2 Mirror the same preference in `.github/copilot-instructions.md` and `docs/quality.md` — verify docs state
      scopes are encouraged, not allowlist-enforced; `commitlint.config.cjs` unchanged (no `scope-enum`)

## 4. Validate

- [ ] 4.1 Ensure delta specs match the shipped contract — verify `openspec validate release-cliff-changelog --strict`
