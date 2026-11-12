## Context

See `proposal.md`. Today five `scripts/install-*.sh` files share the same skeleton with per-tool asset/arch quirks.
Reusable workflows and postCreate already call one script per tool; CI must keep that one-step-per-tool shape. Locked
explore: include kubeconform; Dockerfile stays inline curl
([#374](https://github.com/fairagro/m4.2_middleware_devinfra/issues/374)); registry as bash `case` in one driver.

## Goals / Non-Goals

**Goals:**

- One driver + in-script registry for gitleaks, actionlint, kubeconform, cst, git-cliff
- Net fewer files (delete per-tool install scripts; no shims)
- Preserve pin SoT, fail-closed, sudo-safe `versions.env` load

**Non-Goals:**

- Dockerfile calling the driver (#374)
- Renovate/customManager or pin-name changes
- Unifying non-GitHub-release installs (npm globals, apt packages)

## Decisions

1. **`install-pinned-tool.sh <tool>` + bash `case`** — no separate manifest format; tool quirks stay next to the
   download logic (CST raw binary + `cst` symlink; git-cliff sha512; gitleaks `x64` vs actionlint `amd64`).
2. **No shims** — update every call site in the same change; consumers pick up via sync.
3. **Allowlist the driver on `foundation`** — product union and Infra both receive it; drop the five old paths
   (including python-product `install-cst` / `install-git-cliff` entries).
4. **Dockerfile dual path documented** — image build keeps inline `RUN`; docs point at #374 for optional convergence.

## Risks / Trade-offs

- [Missed call site] → Grep for `install-{gitleaks,actionlint,kubeconform,cst,git-cliff}.sh` in apply; fail CI if any
  remain outside archive/docs history.
- [Registry grows awkward] → Accept for five tools; split only if a later tool needs a real DSL.
- [sudo + DEST] → Keep `*_INSTALL_DIR` / default `/usr/local/bin` behavior equivalent to today’s scripts.

## Migration Plan

1. Land driver + call-site + allowlist + docs on Devinfra; delete old scripts in the same commit set.
2. Products/Infra pick up via sync; no dual-run period.
3. Rebuild Dev Containers only if docs claim image behavior changed (it should not for this MVP).

## Open Questions

None for propose — #374 tracks Dockerfile-via-driver.
