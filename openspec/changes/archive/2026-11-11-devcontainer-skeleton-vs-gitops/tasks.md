## 1. Documentation

- [x] 1.1 Update `docs/sync.md` with Dev Container overlay model, Infra fat-image ownership until adoption, and
      pin-ownership buckets (shared: Helm/minikube today/git-lfs eligible; python-product; Infra: argocd/kind/ct); link
      #364 / API #670 for minikube→kind — verify prose matches delta specs and markdownlint/Prettier pass on the file
- [x] 1.2 Update `docs/devcontainer.md` to state the shared image is python-product SoT, Infra keeps its GitOps image
      until adoption, pin buckets + deferred kind swap — verify cross-links from sync.md work and lint passes
- [x] 1.3 Add a short cross-link in `docs/quality.md` or `docs/synced-paths.yaml` header comments only if needed so
      operators find the split — verify no duplicate conflicting ownership claims

## 2. Sync guards

- [x] 2.1 Extend `scripts/tests/test_sync_products_profiles.py` so Infra effective allow / resolve_files exclude
      `.devcontainer/` (and product union still includes it) — verify
      `uv run pytest scripts/tests/test_sync_products_profiles.py` passes
- [x] 2.2 Confirm `docs/synced-paths.yaml` already keeps `.devcontainer/**` on `python-product` only; adjust comments if
      the profile header should mention the #352 contract — verify no allowlist path move onto
      foundation/gitops/infra-consumer

## 3. Validate

- [x] 3.1 Run `openspec validate devcontainer-skeleton-vs-gitops --strict` (or project equivalent) and Prettier on
      touched docs — verify validate succeeds and `npm run format:md:check` would pass for edited Markdown
