## 1. Tooling pins and cliff config

- [ ] 1.1 Add `GIT_CLIFF_VERSION` to `versions.env` and install git-cliff on `PATH` in the shared Dev Container image —
      verify `git-cliff --version` matches the pin in a rebuilt or documented install path
- [ ] 1.2 Add shared `cliff.toml` (tag/bump settings suitable for Docker and Helm overrides) — verify
      `git cliff --bumped-version` dry-run against this repo (or a fixture) exits successfully with Conventional sample
      history

## 2. Detect wrapper + workflows

- [ ] 2.1 Add `scripts/detect-version-bump.sh` (or equivalent) wrapping git-cliff for surface-specific tag patterns;
      fail closed on errors — verify non-zero exit when cliff/tag resolution fails; success prints base semver
- [ ] 2.2 Wire `version_bump` `auto|major|minor|patch` (default `auto`) into `reusable-build.yml` (and Helm final /
      pre-release base bump as applicable); keep RC/PEP440 suffix on `build/*` — verify input default and case paths in
      workflow YAML
- [ ] 2.3 Update `docs/ci.md` Release snippets / input tables for `auto` + Conventional Commits / R1 / F1 — verify
      Prettier / markdownlint on touched docs

## 3. Conventional Commits enforcement + editors

- [ ] 3.1 Add commitlint (conventional config) to root npm SoT + pre-commit hook; allow Renovate `deps:` — verify bad
      message fails hook; `deps:`-style allowed message passes
- [ ] 3.2 Configure synced `.vscode/settings.json` (and Copilot instructions as needed) so **Cursor and VS Code**
      commit-message generation target Conventional Commits — verify keys/docs mention both editors
- [ ] 3.3 Document mapping + enforcement + editor UX in `docs/quality.md` (and cross-link from `docs/ci.md`) — verify
      Prettier / markdownlint

## 4. Sync allowlist

- [ ] 4.1 Allowlist new shared files (`cliff.toml`, detect script, commitlint config, any new instruction fragments) in
      `docs/synced-paths.yaml` / sync inventory — verify paths appear under `allow`

## 5. Validate

- [ ] 5.1 Ensure all delta specs match the shipped impl — verify `openspec validate release-auto-version-bump --strict`
