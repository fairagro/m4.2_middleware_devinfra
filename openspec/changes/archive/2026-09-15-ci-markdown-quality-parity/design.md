## Context

See proposal.md — Why. `reusable-code-quality.yml` today is Python-only. Hooks already call `npm run lint:md` / format
scripts; Dev Container installs Prettier/markdownlint globally from `versions.env`, but CI and product sync lack
`package.json` / lockfile. Locked approach: Option A + sync those manifests.

## Goals / Non-Goals

**Goals:**

- Same Prettier/markdownlint pass/fail in reusable CI as hooks for the same tree/configs.
- Clear product adoption via sync allowlist + docs.
- Fail closed without Node manifest.

**Non-Goals:**

- Separate companion markdown workflow (Option B).
- Optional `skip_markdown` input in MVP.
- Changing markdown rule content (configs stay as-is).
- Syncing `node_modules`.

## Decisions

1. **Same job, not companion workflow** — keeps one required check name; matches parity story.

2. **`actions/setup-node` + `npm ci`** — use Node major from `package.json` `engines.node` (or `versions.env`
   `NODE_VERSION` when easy to wire). Cache npm. Run `npm run format:md:check` then `npm run lint:md` after checkout,
   before or after Python steps (order: after checkout; prefer before heavy Python to fail fast on md — either is fine;
   prefer **after checkout / early**).

3. **Sync `package.json` + `package-lock.json`** — required for caller `npm ci`. Document in `docs/sync.md` inventory
   and `docs/ci.md` briefly. Renovate already may touch npm deps in Devinfra; products get pins via sync.

4. **Fail closed** — no soft-skip if manifest missing when `skip: false`.

5. **Specs** — delta `reusable-ci-workflows`, `shared-quality-tooling`, `synced-consumer-paths`.

## Risks / Trade-offs

- [Risk] Products break until next sync copies manifests → Mitigation: document; sync PR lands package files.
- [Risk] Product-local `package.json` conflicts → Mitigation: allowlist means Devinfra is SoT; products should not fork
  scripts; open follow-up if a product already has a conflicting root manifest.
- [Trade-off] Longer CI (npm ci) → Accepted for parity.

## Migration Plan

Ship workflow + allowlist + docs together. After merge, product sync brings manifests; callers using reusable
code-quality gain markdown gates automatically. No workflow input changes required for MVP.
