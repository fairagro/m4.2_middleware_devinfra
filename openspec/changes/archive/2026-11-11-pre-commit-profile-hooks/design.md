## Context

#351 explore locked composable fragments first; apply revised to **option B** (user): two full configs, **no**
`compose-pre-commit.py` / `.pre-commit.d/`. MVP C (products + Infra wiring) and hook map remain. Drop obsolete lettered
“wave” adopt labels from live SoT.

## Goals / Non-Goals

**Goals**

- Product root = full hook set; Infra root = foundation + gitops only
- Sync profiles wire the correct file(s) per target
- Docs describe duplication trade-off for shared hooks
- Live SoT free of obsolete wave labels

**Non-Goals**

- Fragment merge / generator script
- actionlint (#353) / kubeconform (#348) / Renovate on Infra (#354)
- Rewriting archive OpenSpec history

## Decisions

1. **Two files** — `.pre-commit-config.yaml` (products + Devinfra) and `.pre-commit-config.infrastructure.yaml` (Infra).
2. **Duplication** — foundation/gitops hooks that appear in both are edited in both places; document in
   `docs/quality.md`.
3. **Sync** — product root on `python-product`; Infra root + helpers on `foundation`; `run-helm-lint.sh` on `gitops`;
   targets: products foundation+python-product+gitops; infrastructure foundation+gitops.
4. **Infra install** — copy/symlink Infra file to `.pre-commit-config.yaml` or `PRE_COMMIT_CONFIG_FILE`.

## Risks / Trade-offs

- **[Trade-off] Dual edit of shared hooks** → Accepted vs maintaining a compose script.
- **[Risk] Drift between the two files** → Docs + PR review; optional later check (out of scope unless cheap).

## Migration Plan

1. Land Infra config + allowlist moves; products keep existing root.
2. Document Infra install; operators unskip Infra sync when ready.

## Open Questions

- None.
