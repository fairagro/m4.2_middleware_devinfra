# Design: remove Git LFS, keep pre-push quality hooks

## Context

See proposal.md — Why. Explore lock-in for issue #39: **A1** rename capability to `shared-git-hooks`; **B1**
`setup-git-hooks.sh` + stub at old name; **C1** delete LFS `post-*` hooks; **D1** drop `git-lfs` from shared image.
sql-to-arc still needs LFS → product-local install after sync (not thin `devcontainer.json` alone).

## Goals / Non-Goals

**Goals:**

- Shared happy path: no LFS dependency; pre-push still runs pre-commit pre-push (pytest/CST as configured)
- Clear sync migration: new script name + stub; docs for product-local LFS

**Non-Goals:**

- Implementing sql-to-arc’s product Dockerfile/postCreate LFS install in this repo
- Changing pre-commit hook stages or CST/pytest content
- Supporting unofficial host auto-install of git-lfs

## Decisions

### D1 — Capability rename (A1)

New main capability folder `shared-git-hooks`. Retire `shared-git-hooks-lfs` via REMOVED requirements + delete/replace
main spec at archive. Avoid keeping a misleading `*-lfs` capability name.

### D2 — Installer (B1)

| Path                         | Role                                                                  |
| ---------------------------- | --------------------------------------------------------------------- |
| `scripts/setup-git-hooks.sh` | Copy `scripts/git-hooks/pre-push` → `.git/hooks/`; no `git-lfs` check |
| `scripts/setup-git-lfs.sh`   | Stub: print rename guidance, exec or exit directing to new script     |

Stub keeps old sync paths from failing silently into “must have LFS”.

### D3 — Hooks (C1)

- `pre-push`: only buffer stdin → pre-commit `hook-impl --hook-type=pre-push` (same uv/venv/PATH fallbacks as today)
- Delete `post-checkout`, `post-commit`, `post-merge`

### D4 — Image + postCreate (D1)

Remove `git-lfs` apt package and `git lfs install --system` from Dockerfile. postCreate invokes
`./scripts/setup-git-hooks.sh`.

### D5 — Product-local LFS

Docs (`docs/devcontainer.md` / quality): products that need LFS (sql-to-arc) install `git-lfs` in a **product-owned**
path that sync does not overwrite (e.g. product postCreate snippet or non-synced Dockerfile fragment). Shared base does
not ship LFS.

## Risks / Trade-offs

- [sql-to-arc breaks until product installs LFS] → Mitigation: sync note + stub; follow-up on product via #13
- [Old clones keep LFS hooks in `.git/hooks`] → Mitigation: re-run setup script / rebuild container
- [Stub forever] → Acceptable until sync adopts new name; may remove stub in a later cleanup

## Migration Plan

1. Land scripts/hooks/Dockerfile/docs/specs on the issue branch.
2. Sync (#13): products pick up `setup-git-hooks.sh`; sql-to-arc adds local LFS before relying on LFS assets.
3. Rebuild Dev Containers after merge.
