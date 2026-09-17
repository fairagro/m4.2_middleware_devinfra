## 1. Shared base Dockerfile

- [ ] 1.1 Document `SECONDARY_BINARY_NAME`, `SECONDARY_PYINSTALLER_IMPORT`, `SECONDARY_PYINSTALLER_ENTRY`, and
      `SECONDARY_ONEFILE` in the ARG header of `docker/Dockerfile.product-app.base` (empty name = skip) and verify the
      header lists them next to the primary binary ARGs
- [ ] 1.2 Declare the secondary ARGs on `binary-builder` and, when `SECONDARY_BINARY_NAME` is non-empty, run a second
      PyInstaller build (default `--onefile`, `--onedir` when `SECONDARY_ONEFILE=false`) using the same entry-resolution
      pattern as primary; verify empty secondary leaves the primary-only `pyinstaller --onedir` path unchanged in the
      Dockerfile
- [ ] 1.3 Fail closed when secondary name is set but neither import nor a valid entry resolves; verify the RUN block
      emits a clear ERROR and exits non-zero (same style as primary)

## 2. Docs and examples

- [ ] 2.1 Document the secondary ARG contract, no-op default, onefile vs onedir, and last-stage COPY paths in
      `docs/ci.md` (product-app Bake section); note product follow-up to drop local healthcheck Dockerfiles after sync;
      verify `npm run lint:md` is clean for touched docs
- [ ] 2.2 Update `docker/examples/docker-bake.hcl.example` and/or `Dockerfile.last.example` with commented secondary
      args and an optional secondary COPY; verify examples still illustrate the single-primary happy path by default

## 3. Validate

- [ ] 3.1 Run `openspec validate product-app-secondary-binary --strict` and fix any reported issues until it passes
