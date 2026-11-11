## Context

See `proposal.md`. Mirror gitleaks/actionlint: `*_VERSION` in `versions.env`, `scripts/install-*.sh`, Dockerfile `ARG` +
`RUN`, Renovate customManager. Unlike actionlint, kubeconform is **opt-in** for consumers — no foundation pre-commit
hook and no reusable-code-quality step in this change. #347 locked it as foundation pin/runner tooling; consumer matrix
wiring stays on infra#75.

## Goals / Non-Goals

**Goals:**

- One `KUBECONFORM_VERSION` SoT for Dev Container and consumer CI install paths
- Thin runner usable from a consumer script after `helm template` (stdin or files; flag pass-through)
- Foundation sync of install + runner so Infra can adopt without product hook hard-fail

**Non-Goals:**

- Wiring kubeconform into `run-helm-lint.sh` or shared pre-commit
- Fleet-default Argo CRD schema packs / `-ignore-missing-schemas` policy
- Live cluster / server-side dry-run
- Infra template-matrix implementation (infra#75)

## Decisions

1. **Foundation, not gitops-only** — matches #347 lock-in; pin + helpers belong with other shared install/runners; chart
   matrix stays consumer-local.
2. **Bake into product Dev Container** — same ergonomics as gitleaks/actionlint; unused on pure-Python paths is
   acceptable binary cost. Infra keeps its own image and uses install script + synced `versions.env`.
3. **Thin runner, not chart discovery** — avoids coupling to `charts/` migration (#349) and CRD policy; consumers own
   render + flags.
4. **Renovate customManager like actionlint** — `yannh/kubeconform` GitHub releases; pin keeps leading `v` via
   `autoReplaceStringTemplate`.

## Risks / Trade-offs

- [Product image grows another CLI] → Accepted for foundation parity; document as shared-eligible pin.
- [Consumers pass bad CRD flags] → Docs only; fail closed is kubeconform’s behavior, not the runner’s job.
- [OpenVSX/asset naming drift] → Install script fails closed; Renovate/datasource catches version bumps.

## Migration Plan

1. Land pin + install + image + runner + allowlist + docs on Devinfra; products pick up via sync.
2. Link from infra#75 / infra#80 when Infra wires the matrix (out of this PR).
3. Rebuild Dev Containers after merge.

## Open Questions

None for propose.
