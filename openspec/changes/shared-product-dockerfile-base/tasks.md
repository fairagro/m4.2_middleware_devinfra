# Tasks: shared-product-dockerfile-base

## 1. Shared base Dockerfile

- [ ] 1.1 Add `docker/Dockerfile.product-app.base` with package-builder, binary-builder (ARG-parameterized), and
      `export-binaries` (`/dist`); no product runtime finishing
- [ ] 1.2 Document ARG list in-file and/or docs (toolchain, packages, binary identity, optional builder extras)
- [ ] 1.3 Run hadolint on the base Dockerfile; fix actionable findings

## 2. Examples and docs

- [ ] 2.1 Add example last-stage + `docker-bake.hcl` stubs showing A4 `contexts = { … = "target:…" }`
- [ ] 2.2 Update `docs/ci.md` / `docs/quality.md`: sync boundaries, Bake-only contract, strict cutover (no monolith),
      structure expectations for the three products
- [ ] 2.3 Point README layout (if needed) at the new `docker/` base / examples

## 3. Reusable CI (B2-strict)

- [ ] 3.1 Change `reusable-build.yml` to Buildx Bake (base + last); preserve tags, build-args from `versions.env`, GHA
      cache, and check artifact contract; remove monolith `file: docker/Dockerfile.$COMPONENT` path
- [ ] 3.2 Update `reusable-release.yml` build-from-source (and any rebuild) to Bake; drop monolith `docker build -f`
      instructions

## 4. Validate

- [ ] 4.1 `npm run format:md` / `lint:md` on touched docs; hadolint on Dockerfiles
- [ ] 4.2 Spot-check docs scenarios (sync boundary, strict cutover, Bake) against the specs
