# Design: shared-product-dockerfile-base

## Context

See proposal.md — Why. Explore lock-ins for #36: **A4** (Buildx Bake + `contexts`), **B2** (base + docs + example + CI
Bake), **B2-strict** (no monolith fallback), **C2** (package + binary-builder + export in base; runtime last stage),
**M=mixed** (builder extras in base; runtime finishing in last), **R=yes** (release docs/path aligned), **P**=
`docker/Dockerfile.product-app.base`, **S**= document cutover; adoption via Wave C / #13. Today `reusable-build.yml`
uses `docker/build-push-action` with `file: docker/Dockerfile.${{ matrix.component }}`. Release bodies still echo
monolith `docker build -f`.

## Goals / Non-Goals

**Goals:**

- Land a real shared base Dockerfile with documented ARGs and `export-binaries`
- Wire reusable build to Bake-only; keep artifact tag/SBOM contract unchanged
- Align release “build from source” text (and any rebuild) with Bake
- Document sync boundaries and strict cutover

**Non-Goals:**

- Migrating API / sql-to-arc / harvester Dockerfiles in this PR
- Jinja or template engines
- Monolith compatibility mode
- Changing reusable-check artifact names

## Decisions

1. **Compose = A4 Bake** Base target builds through `export-binaries`; last Dockerfile uses
   `# syntax=docker/dockerfile:1.4` and `FROM <context>` / `COPY --from=…`. _Alternatives:_ A1 cat, A2 two-step image
   tags — rejected in explore.

2. **B2-strict** No `dockerfile_mode: monolith`. Callers must adopt before bumping workflow ref. _Alternative:_ compat
   default — rejected by user.

3. **C2 + M mixed** Base owns package-builder, binary-builder (ARGs for packages, binary name(s), optional builder
   apk/ODBC download), export to `/dist`. Last owns USER/UID, CMD/ENTRYPOINT, EXPOSE, HEALTHCHECK, git config, runtime
   apk. _Alternative:_ C1/C3 — rejected.

4. **Example stubs in Devinfra** e.g. `docker/examples/Dockerfile.last.example` +
   `docker/examples/docker-bake.hcl.example` (or under `docs/`). Not invoked by Devinfra CST (no product `middleware/`).

5. **Bake invocation in CI** Prefer `docker/bake-action` (or `docker buildx bake`) with a **caller-provided**
   `docker-bake.hcl` path convention documented in `docs/ci.md` (e.g. repo-root `docker-bake.hcl`, target name =
   component). Shared Devinfra may ship only the example HCL; products own real targets. _Alternative:_ generate HCL in
   the workflow from inputs — more magic; defer unless needed.

6. **Release** Update release-body build-from-source snippet to Bake; if release ever rebuilds images, same Bake
   contract.

## Risks / Trade-offs

- **[Risk] Callers bump `@main` before product split → red CI** → Mitigation: loud docs + Wave C / #13 status updates;
  consider release notes on the PR.
- **[Risk] Base ARGs cannot express every PyInstaller quirk** → Mitigation: document supported ARG surface; product may
  keep thin last stage only — extreme cases deferred to product follow-ups, not fork of base without upstreaming.
- **[Risk] Hadolint on new Dockerfiles** → Mitigation: run hadolint in apply; fix or justify.
- **[Trade-off] Strict over compat** → Accepted; forces coordinated adoption.

## Migration Plan

1. Land base + examples + docs + Bake-only workflows on issue branch; draft PR `Fixes #36`.
2. Update product Wave C issues (already mention #12/#28) with Bake cutover note when this merges.
3. Products adopt base+last+bake, then pin/bump reusable workflow ref.
4. Rollback: revert workflow to monolith `file:` (emergency only); base file can remain.

## Open Questions

None for propose (lock-ins closed; remaining ARG names can be fixed during apply against the three product Dockerfiles).
