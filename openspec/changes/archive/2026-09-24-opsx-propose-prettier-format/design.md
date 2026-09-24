## Context

See proposal.md — Why. Fleet Prettier gates product-owned `openspec/changes/**`; opsx skill/command trees are already
ignored (#241). Propose currently has no mandatory format step, so freshly written planning Markdown fails `prettier-md`
/ CI.

Opsx propose skill/command files are OpenSpec-CLI managed (not on the Devinfra sync allowlist). Patching them in this
repo is the agent contract for Devinfra and a template for products; `openspec update` can regenerate them.

## Goals / Non-Goals

**Goals:**

- Propose skill + `/opsx-propose` command: final Prettier write on the change directory
- Synced docs/principles note the guarantee and the `openspec update` overwrite risk
- Spec delta on `shared-quality-tooling` so archive folds the contract into main specs

**Non-Goals:**

- Ignoring `openspec/changes/**` in Prettier
- Changing markdownlint policy for `openspec/**` (already ignored)
- Patching every opsx skill (apply/archive/update) in this slice — propose is the generation hot path; apply/update MAY
  reuse the same one-liner in a follow-up if needed
- Upstream OpenSpec CLI release (document only; optional later)

## Decisions

1. **Skill step, not ignore-list** — Preferred AC: generation path formats. Keeps planning docs Prettier-owned.
2. **Scoped write, not full-repo `format:md`** — `prettier --write "openspec/changes/<name>/**/*.{md,mdc}"` (or
   `changeRoot` from status JSON) avoids rewriting unrelated dirty trees mid-propose.
3. **Patch skill + command** — Agents enter via `/opsx-propose` command or the skill file; keep both aligned. GitHub
   prompt twin only if it duplicates the procedure.
4. **Docs + overwrite caveat** — `docs/quality.md` / `principles.global.md`: one short paragraph; do not pretend the
   patch survives `openspec update` without re-apply.
5. **ADDED requirement** on `shared-quality-tooling` rather than inventing a new capability or bloating
   `global-principles`.

## Risks / Trade-offs

- [Risk] `openspec update` overwrites the skill → Mitigation: document re-apply; consider upstream later.
- [Risk] Products still on unpatched opsx skills → Mitigation: synced principles/docs; copy patch or wait for update
  that includes it.
- [Risk] Prettier unavailable on PATH in some host clones → Mitigation: same as existing `prettier-md` hook (`npm` / Dev
  Container pins); fail loudly if missing.

## Migration Plan

1. Land skill/command + docs + delta in Devinfra.
2. Products: pull docs via sync; refresh or hand-patch opsx propose skill/command until CLI ships the step.
3. No rollback beyond reverting the skill text.
