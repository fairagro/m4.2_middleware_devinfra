# Tasks: shared Renovate config + workflow

## 1. Config and workflow

- [ ] 1.1 Add root `renovate.json` seeded from API config; extend regex/`packageRules` for Devinfra `versions.env`
      toolchain pins
- [ ] 1.2 Add `.github/workflows/renovate.yml` (schedule + dispatch + push on config; Action + `RENOVATE_TOKEN`;
      single-repo)

## 2. Docs and allowlist

- [ ] 2.1 Add `docs/renovate.md` (token secret, local dry-run, Dependabot migration C1, #13 adoption)
- [ ] 2.2 Link from README Docs (+ brief pointers in `docs/devcontainer.md` / `docs/ci.md`)
- [ ] 2.3 Add `renovate.json` and `.github/workflows/renovate.yml` to `docs/synced-paths.global.md`

## 3. Validate

- [ ] 3.1 Local `renovate` dry-run / config validate against pinned CLI when feasible
- [ ] 3.2 Format/lint touched Markdown; spot-check workflow references `RENOVATE_TOKEN`
