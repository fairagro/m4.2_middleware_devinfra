## 1. PATH + wrappers

- [x] 1.1 Update `.devcontainer/devcontainer.json` `remoteEnv.PATH` to prepend `${workspaceFolder}/.venv/bin` and
      `${workspaceFolder}/scripts/bin`
- [x] 1.2 Add thin `scripts/bin/k` and `scripts/bin/d` wrappers (exec real kubectl/docker; no tokens; no bashrc)
- [x] 1.3 Ensure wrappers are executable and covered by existing `scripts/bin` sync allowlist (or extend
      `docs/synced-paths.yaml` if needed)
- [x] 1.4 Add image bash-completion entries for `k`/`d` in `.devcontainer/Dockerfile` (reuse kubectl/docker completion
      functions; no `~/.bashrc`)

## 2. postCreate SOPS decrypt

- [x] 2.1 In `scripts/devcontainer-post-create.sh`, after GPG import (or adjacent), optionally decrypt
      `.env.integration.enc` → `.env` (skip if `.env` non-empty / ciphertext absent / sops missing; never fail create)
- [x] 2.2 Confirm Devinfra `.gitignore` ignores `.env` (add if missing)

## 3. Docs

- [x] 3.1 Update `docs/devcontainer.md`: bashrc-free contract, `remoteEnv.PATH`, wrappers, postCreate decrypt; deprecate
      product `load-env.sh` / bashrc wiring; note product follow-ups
- [x] 3.2 Light cross-links from `docs/conventions.md` and/or `docs/sync.md` inventory if PATH/scripts need mentioning
- [x] 3.3 Format/lint only touched Markdown
- [x] 3.4 Document image-provided `k`/`d` bash completion (rebuild required)

## 4. Validate + follow-ups

- [x] 4.1 `openspec validate shared-shell-init-no-bashrc --strict` (and smoke: wrappers resolve when on PATH)
- [x] 4.2 After user commits / on draft-PR cadence: open linked follow-up issues for product adopt (at least harvester,
      API, sql_to_arc) via create-issue skill — drop bashrc/`load-env.sh`, align `remoteEnv` (created: #103 harvester,
      #104 API, #105 sql_to_arc — sub-of #58)
