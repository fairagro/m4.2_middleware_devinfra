## 1. Sync allowlist

- [x] 1.1 Add `package.json` and `package-lock.json` to `docs/synced-paths.yaml` allow
- [x] 1.2 Note them in `docs/sync.md` inventory (markdown / Node toolchain)

## 2. Reusable CI

- [x] 2.1 Add Node setup + `npm ci` + `format:md:check` + `lint:md` steps to `reusable-code-quality.yml` (respect
      `skip`; fail closed without manifest)
- [x] 2.2 Document the markdown CI steps in `docs/ci.md` (reusable-code-quality section)

## 3. Parity docs

- [x] 3.1 Update `docs/quality.md` parity table: Prettier/markdownlint CI = yes (not commit-stage-only)
- [x] 3.2 Adjust principles / quality wording only if it still claims commit-stage substitutes for CI

## 4. Validate

- [x] 4.1 `openspec validate --strict`; format/lint Markdown; sanity-check workflow YAML
