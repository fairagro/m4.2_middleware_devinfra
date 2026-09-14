## Context

See proposal.md — Why. Today Devinfra `remoteEnv` only prepends `scripts/bin`; `.venv/bin` is exported inside the
postCreate process only. Products still use `load-env.sh` + bashrc for PATH, aliases, and SOPS. Personal tokens already
use PATH wrappers without bashrc (`personal-token-helpers`). Issue #58 lock-in: no home bashrc mutation; no shared
`load-env.sh`; `.env` file decrypt is enough (no per-shell export); product adopt via follow-up issues.

## Goals / Non-Goals

**Goals:**

- One bashrc-free contract for PATH + kubectl/docker short names + optional postCreate `.env` materialization.
- Spec + docs + Devinfra implementation; allowlist any new `scripts/bin` wrappers.
- Clear product migration story (follow-ups), not silent dual systems forever in docs.

**Non-Goals:**

- Migrating harvester / API / sql_to_arc / infrastructure trees in this PR.
- Auto-`source` of `.env` into interactive shells (direnv / image `/etc/bash.bashrc`).
- Restoring bashrc token loading; embedding hook/venv repair in a shell-init script.
- Extra kubectl convenience aliases beyond `k` / `d` wrappers (`kga`, `kda`, …) unless already trivial — defer to
  product overlays or a later issue.

## Decisions

1. **PATH via `remoteEnv`, not bashrc**  
   VS Code/Cursor applies `remoteEnv` to integrated terminals and remote processes. Prefer extending existing
   `PATH": "${workspaceFolder}/scripts/bin:${containerEnv:PATH}"` to include `.venv/bin`.  
   _Alternative rejected:_ `setup-bashrc-load-env.sh` (user goal: no `~/.bashrc` mutation).

2. **No `load-env.sh`**  
   With PATH + wrappers + postCreate decrypt, a sourced script is unnecessary fleet surface.  
   _Alternative rejected:_ shared `load-env.sh` “for optional source” (would invite bashrc rewiring).

3. **Aliases → `scripts/bin/k` and `scripts/bin/d`**  
   Same discovery model as `gh`/`git` wrappers, but without token loading — thin `exec` of real binary via
   `command -v -p` / `/usr/bin` fallback pattern (simplified vs token wrappers).  
   _Alternative rejected:_ bash `alias` in profile.d (still a shell-rc story).

4. **SOPS decrypt in postCreate only**  
   Mirror product behavior for file presence, skip if `.env` non-empty, soft-fail without aborting create. Do not
   `set -a; source .env` into bashrc. `dev_environment` / tests read the file.  
   _Alternative deferred:_ image-level hook or direnv for shell export.

5. **Devinfra `devcontainer.json` updated in-repo; products via follow-ups**  
   `devcontainer.json` is product-owned (sync exclude). Docs MUST require the PATH line; Devinfra’s own overlay is the
   reference implementation.

6. **Follow-up issues**  
   After implement (or with draft PR), open linked issues per product repo to drop bashrc/`load-env.sh` and align
   `remoteEnv` + consume synced wrappers.

## Risks / Trade-offs

- **[Risk] `.venv` missing before first `uv sync`** → Mitigation: postCreate still syncs; empty prepend is harmless;
  after sync, new terminals get tools. Rebuild/re-attach if an old terminal retained a stale PATH.
- **[Risk] Host `bash` outside Dev Container** → Mitigation: contract is Dev Container–first (same as token wrappers);
  host users keep their own env.
- **[Risk] Products keep dual load-env until follow-ups merge** → Mitigation: docs mark load-env deprecated; create
  follow-up issues; sync still delivers wrappers/postCreate for gradual adopt.
- **[Risk] Decrypt writes secrets to workspace `.env`** → Mitigation: same as today’s product pattern; ensure `.env`
  stays gitignored (product responsibility; note in docs if missing in Devinfra).

## Migration Plan

1. Land Devinfra change (remoteEnv, wrappers, postCreate, docs, allowlist, OpenSpec).
2. Sync allowlisted paths to products.
3. Per-product follow-up: set `remoteEnv.PATH`, remove bashrc load-env lines / `setup-bashrc-*`, delete or shrink
   `load-env.sh`, verify `.env` gitignore + postCreate decrypt.
4. Rollback: revert Devinfra PR; products can temporarily keep old load-env until sync of the revert.

## Open Questions

None — product follow-up issue titles/bodies can be drafted at apply/PR time without changing this design.
