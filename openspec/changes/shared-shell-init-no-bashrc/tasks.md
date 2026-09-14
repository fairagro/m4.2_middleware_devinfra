## 1. PATH + wrappers

- [ ] 1.1 Update `.devcontainer/devcontainer.json` `remoteEnv.PATH` to prepend `${workspaceFolder}/.venv/bin` and
      `${workspaceFolder}/scripts/bin`
- [ ] 1.2 Add thin `scripts/bin/k` and `scripts/bin/d` wrappers (exec real kubectl/docker; no tokens; no bashrc)
- [ ] 1.3 Ensure wrappers are executable and covered by existing `scripts/bin` sync allowlist (or extend
      `docs/synced-paths.yaml` if needed)

## 2. postCreate SOPS decrypt

- [ ] 2.1 In `scripts/devcontainer-post-create.sh`, after GPG import (or adjacent), optionally decrypt
      `.env.integration.enc` → `.env` (skip if `.env` non-empty / ciphertext absent / sops missing; never fail create)
- [ ] 2.2 Confirm Devinfra `.gitignore` ignores `.env` (add if missing)

## 3. Docs

- [ ] 3.1 Update `docs/devcontainer.md`: bashrc-free contract, `remoteEnv.PATH`, wrappers, postCreate decrypt; deprecate
      product `load-env.sh` / bashrc wiring; note product follow-ups
- [ ] 3.2 Light cross-links from `docs/conventions.md` and/or `docs/sync.md` inventory if PATH/scripts need mentioning
- [ ] 3.3 Format/lint only touched Markdown

## 4. Validate + follow-ups

- [ ] 4.1 `openspec validate shared-shell-init-no-bashrc --strict` (and smoke: wrappers resolve when on PATH)
- [ ] 4.2 After user commits / on draft-PR cadence: open linked follow-up issues for product adopt (at least harvester,
      API, sql_to_arc) via create-issue skill — drop bashrc/`load-env.sh`, align `remoteEnv`
