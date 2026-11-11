## 1. Pin + install + image

- [x] 1.1 Add `KUBECONFORM_VERSION` to `versions.env` and a Renovate customManager entry (actionlint/gitleaks pattern) —
      verify Renovate matchString would capture the pin
- [x] 1.2 Add `scripts/install-kubeconform.sh` (fail closed without pin; install to PATH) — verify
      `bash scripts/install-kubeconform.sh` installs the pinned binary in Dev Container
- [x] 1.3 Wire Dockerfile `ARG`/`RUN` + compose build-arg for kubeconform — verify image rebuild docs mention the pin
- [x] 1.4 Add `scripts/run-kubeconform.sh` (file args and/or stdin; flag pass-through; fail closed if binary missing; no
      helm/chart discovery) — verify a sample manifest or stdin run exits 0 against a trivial Deployment YAML

## 2. Sync allowlist + docs

- [x] 2.1 Allowlist `scripts/install-kubeconform.sh` and `scripts/run-kubeconform.sh` under `foundation` in
      `docs/synced-paths.yaml` — verify profile tests still pass
- [x] 2.2 Document pin/install/runner vs helm-lint (opt-in; CRD policy consumer-owned) in `docs/quality.md` and briefly
      in `docs/devcontainer.md` — verify Prettier/markdown checks on touched docs
- [x] 2.3 Confirm `scripts/run-helm-lint.sh` and shared helm-lint hooks do not invoke kubeconform — verify no new
      required call sites
- [x] 2.4 `openspec validate kubeconform-foundation --strict` + Prettier on change Markdown — verify validate succeeds

## Workflow follow-up

- After apply + draft PR: link infra#75 / infra#80 when ready for consumer matrix wiring (comment only; not blocking
  archive)
- Archive this change on the final issue-fixer `go` after the draft PR exists
