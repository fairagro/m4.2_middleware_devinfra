## Context

Issue [#174](https://github.com/fairagro/m4.2_middleware_devinfra/issues/174). Trivy in `reusable-check` covers image /
SBOM CRITICAL/HIGH. There is no lockfile CVE gate in hooks or `reusable-code-quality`. Fleet is uv-first (`UV_VERSION`
in `versions.env`). `uv audit` is available on the current pin but marked experimental/preview. Lock-in: **A1**
`uv audit`, **B2** hooks+CI, **C1** fail any finding + ID ignores (C2 severity filter unavailable on `uv audit`), **D1**
Trivy stays image gate, **D2** enable `UV_MALWARE_CHECK` on fleet sync entrypoints.

## Goals / Non-Goals

**Goals:**

- Primary Python lockfile/env CVE gate via `uv audit --frozen` in commit-stage and reusable code-quality
- Matching fail bar hooks ↔ CI; named IDE exception (network / no extension)
- Product-owned ignore overlay for advisory IDs without patching synced pre-commit YAML
- Malware check on code-quality and Dev Container post-create `uv sync`
- Docs: uv audit vs Trivy vs malware check; preview caveat; `SKIP` / offline note for hooks

**Non-Goals:**

- pip-audit or osv-scanner
- CRITICAL/HIGH-only filter for `uv audit`
- Changing Trivy severity policy in `reusable-check`
- Enabling malware check on every product Docker image bake path in this MVP (document recommendation; optional
  follow-up)
- Making `uv audit` non-preview (Astral’s timeline)

## Decisions

1. **Tool = `uv audit` (not pip-audit)** — native `uv.lock`, no export/workspace hash pain; pin already via
   `UV_VERSION`.
2. **Invocation** — thin `scripts/run-uv-audit.sh`: `uv audit --frozen` (+ preview-features flag to silence warning if
   needed); read optional `.uv-audit-ignore` (one advisory ID per line, `#` comments) and pass `--ignore` per ID; exit
   non-zero on findings. Hooks and CI call the script.
3. **Ignore overlay** — `.uv-audit-ignore` on sync `overlays`; absent file = no ignores.
4. **Malware check** — `UV_MALWARE_CHECK=1` on `uv sync` in `reusable-code-quality.yml` and
   `scripts/devcontainer-post-create.sh`. Document local `export UV_MALWARE_CHECK=1` / future `tool.uv` config for
   products. Not a substitute for audit.
5. **Trivy relationship** — docs table: lock/env → uv audit; image → Trivy. Overlap on the same CVE is OK; different
   layers; do not disable Trivy.
6. **Network** — hooks need OSV reachability; document `SKIP=uv-audit` (or hook id) as escape hatch only, same class as
   other network hooks.

## Risks / Trade-offs

- **Preview API** — CLI flags may change; pin `UV_VERSION` and adjust runner when upgrading uv.
- **B2 offline friction** — commit-stage network; mitigated by SKIP docs, not by dropping the hook (user lock-in).
- **Ignore file abuse** — products could blank the gate; review culture + code-review judgment remain.
- **Malware check false sense of security** — only known MAL advisories; cooldown / Renovate still matter (docs only).

## Migration Plan

1. Land runner + hook + CI + post-create env + docs + synced-paths overlay entry.
2. Sync to products; they add `.uv-audit-ignore` only if needed after first failures.
3. Archive OpenSpec; no product overlay inventing required for green empty ignore.

## Open Questions

- (none — C2 dropped for C1; ignore path default `.uv-audit-ignore`)
