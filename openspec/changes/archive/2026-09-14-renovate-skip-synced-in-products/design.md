# Design: renovate-skip-synced-in-products

## Context

One shared `renovate.json` is synced into Devinfra and the three products. Product Renovate must still update
product-local deps (`middleware/` pep621, product Dockerfiles’ image tags, product workflows) while ignoring Devinfra
SoT files and the BuildKit frontend package that Devinfra already tracks.

## Decisions

1. **Repo-scoped `packageRules`** Use `matchRepositories` for the three product full names + `enabled: false`, rather
   than product-local overlays. Keeps a single synced config.
2. **File disables for synced SoT** `matchFileNames` for `versions.env`, `.python-version`,
   `docker/Dockerfile.product-app.base`, `.devcontainer/Dockerfile`, `renovate.json`, `.github/workflows/renovate.yml`.
3. **Package disable for `docker/dockerfile`** Product last stages may contain `# syntax=docker/dockerfile:…`; bumping
   that in every product duplicates Devinfra example/tracker PRs. Disable by `matchPackageNames` in products only.
4. **Docs + spec** Operators learn the split under Adoption in `docs/renovate.md`; `shared-renovate` carries the
   normative requirement.

## Risks / Trade-offs

- After config sync, Renovate may recreate closed product PRs until the new rules are live — close #384/#385-style PRs
  after sync.
- `matchRepositories` must stay accurate if product repo names change.
