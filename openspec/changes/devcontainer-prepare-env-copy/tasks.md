## 1. Script and wiring

- [ ] 1.1 Add `scripts/devcontainer-prepare-env.sh` (`rm -f` + `cp versions.env` → `.devcontainer/.env`); verify it
      unlinks a symlink and produces a regular file
- [ ] 1.2 Set `.devcontainer/devcontainer.json` `initializeCommand` to that script; allowlist the script under
      `python-product` in `docs/synced-paths.yaml`

## 2. Stop tracking symlink

- [ ] 2.1 `git rm .devcontainer/.env`; drop `!.devcontainer/.env` (and its symlink comment) from `.gitignore` — verify
      generated `.env` is ignored

## 3. Docs

- [ ] 3.1 Update `.devcontainer/docker-compose.yml` header, `docs/devcontainer.md`, `docs/renovate.md`, and
      `versions.env` header — verify no “symlink” wording for `.devcontainer/.env`

## 4. Validate

- [ ] 4.1 Run `openspec validate devcontainer-prepare-env-copy --strict` and Prettier on touched Markdown — verify clean
