## Context

See proposal.md — Why. Today secret scan is ggshield via `scripts/run-quality-cli.sh` in commit-stage only; reusable
code-quality does not run it. Fleet already pins release CLIs in `versions.env` with install helpers (e.g. CST,
git-cliff).

## Goals / Non-Goals

**Goals:**

- One local secret scanner (gitleaks) for commit-stage and reusable code-quality.
- Pin + install via `versions.env` / `scripts/install-gitleaks.sh`; remove ggshield from Python quality pins.
- Document allowlist and product migration; keep sync allowlist coherent (`install-gitleaks.sh`, `.gitleaksignore` if
  committed).

**Non-Goals:**

- Enabling GitHub org push protection / native secret scanning (recommend as follow-up; not this change).
- Hybrid GitGuardian dashboard integration.
- Full-history scans on every PR (prefer diff / git mode appropriate for CI cost; history scan MAY be docs-only or
  scheduled later).
- Retyping issue #340 in GitHub UI (implementation treats the locked Discussion as Feature-shaped work).

## Decisions

1. **Binary pin, not Python package** — `GITLEAKS_VERSION` + GitHub releases install (like CST), not
   `quality-tools-pins.txt`.
   - Alternatives: official `gitleaks/gitleaks` pre-commit repo mirror — rejected as second pin channel beside
     `versions.env`.
2. **CI lives in `reusable-code-quality.yml`** — same job products already call; fail closed when `skip: false`.
   - Alternatives: only `reusable-check.yml` — rejected; secret scan is a code-quality gate, not image/SBOM.
3. **Scan mode** — commit-stage: gitleaks pre-commit/protect against the staged set; CI: `gitleaks git` (or documented
   equivalent) on the checkout with allowlist honor.
   - Alternatives: directory-only scan — weaker for git history of the PR tip; full-clone history every run — too slow
     for default PR gate.
4. **Allowlist file** — commit empty or minimal `.gitleaksignore` (or gitleaks config) as SoT when needed; document in
   `docs/quality.md`.
5. **Remove `GITGUARDIAN_API_KEY` from happy-path docs / token helper prompts** when no other GG consumer remains in
   this repo.

## Risks / Trade-offs

- **[Risk] No live secret validation** → Mitigation: rotate on confirmed leak; optional later GitHub push protection.
- **[Risk] False positives block CI** → Mitigation: documented allowlist workflow; start with default rules.
- **[Risk] Product sync lag leaves ggshield + gitleaks mixed** → Mitigation: migration notes; single sync PR per
  product.
- **[Risk] Install arch/OS matrix** → Mitigation: mirror `install-cst.sh` patterns (linux amd64/arm64 in CI/Dev
  Container).

## Migration Plan

1. Land Devinfra change (hook, pin, CI, docs, specs).
2. Sync products (#13); remove product-local ggshield deps if any; unset unused GG secrets.
3. Infra `m4.2_infrastructure#74` adopts the same tool/config.
4. Rollback: revert sync / restore ggshield only if gitleaks blocks releases; prefer allowlist fixes first.
