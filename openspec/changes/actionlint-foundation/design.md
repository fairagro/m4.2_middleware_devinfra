## Context

See `proposal.md`. gitleaks is the template: `*_VERSION` in `versions.env`, `scripts/install-*.sh`, Dockerfile `ARG` +
`RUN`, Renovate customManager, pre-commit `language: system`, reusable-code-quality install-then-run. #351 placed
foundation hooks in both pre-commit roots; #354 has not yet put `versions.env` on Infra.

## Goals / Non-Goals

**Goals:**

- One `ACTIONLINT_VERSION` SoT for Dev Container, commit-stage, and blocking reusable CI
- Foundation coverage on product + Infra pre-commit roots
- Install helper on `foundation` sync so Infra can install once it has a pin source

**Non-Goals:**

- Soft/non-blocking CI
- Separate required GitHub check named only for actionlint
- Shipping `versions.env` to Infra (#354)
- pre-commit `repo: rhysd/actionlint` rev as a second pin

## Decisions

1. **Mirror gitleaks, not pre-commit-rev** — satisfies the single-pin local+pipeline lock-in.
2. **Both pre-commit roots** — foundation set after #351.
3. **Blocking step in `reusable-code-quality.yml`** — same job as other quality gates; skip still honors `skip` input.
4. **Install script on foundation; pin file on python-product** — Infra gets the script via sync; pin arrives with #354
   or a temporary Infra-local `versions.env` fragment (documented, not invented here).

## Risks / Trade-offs

- [Infra hook without pin until #354] → Docs + infra#80 note; install fails closed with clear error.
- [Existing workflow noise fails CI] → Expected for blocking; fix workflows or follow-up suppressions via actionlint
  config if needed (out of MVP unless apply finds blockers in this repo).

## Migration Plan

1. Land pin + image + hooks + CI + docs on Devinfra; products pick up via sync.
2. Comment infra#80: adopt Infra pre-commit root + install script; full pin with #354.
3. Rebuild Dev Containers after merge.

## Open Questions

None for propose — apply may add a minimal `.github/actionlint.yaml` only if this repo’s workflows need config.
