## Context

See `proposal.md` for motivation ([#76](https://github.com/fairagro/m4.2_middleware_devinfra/issues/76)). Explore
lock-ins: complete Feature-PR docs (cancel + `dorny/paths-filter` + skip wiring, aligned with sql-to-arc #101);
release/Helm serialize (`cancel-in-progress: false`); complementary concurrency on **outer** reusables only; nested
bake/push helpers out of MVP; OpenSpec delta on `reusable-ci-workflows`.

## Goals / Non-Goals

**Goals:**

- Document the fleet-recommended Feature-PR and release concurrency patterns in `docs/ci.md`
- Add matching complementary `concurrency` to the listed outer Devinfra reusables
- Spec the contract so archive folds into `reusable-ci-workflows`

**Non-Goals:**

- Concurrency on nested `reusable-docker-bake` / `reusable-docker-registry-push` / `reusable-helm-oci-push`
- Changing `skip` semantics or moving `detect-changes` into Devinfra
- Implementing product Feature-PR YAML in this repo

## Decisions

### D1: Outer reusables only

**Choice:** code-quality, build, check, release, helm-release, helm-pre-release, registry-retry.

**Alternative:** also nest helpers — deferred; outer groups already bound product-facing calls.

### D2: Group expression

```yaml
concurrency:
  group: ${{ github.repository }}-<workflow-file-stem>-${{ github.event.pull_request.number || github.ref }}
  cancel-in-progress: <true|false>
```

Use a fixed stem per file (e.g. `reusable-build`) so groups do not collide across reusables. PR number when present
keeps Feature-PR cancel scoped; `github.ref` covers dispatch/tag release callers.

### D3: Cancel policy

| Reusable                                                | `cancel-in-progress` |
| ------------------------------------------------------- | -------------------- |
| code-quality, build, check                              | `true`               |
| release, helm-release, helm-pre-release, registry-retry | `false`              |

### D4: Docs path filter defaults

Mirror sql-to-arc’s `code` filter as the suggested default (`middleware/**`, lock/pyproject, `docker/**`,
`docker-bake.hcl`, `.github/**`, `scripts/**`, quality configs, `versions.env`) and note product extensions (`stubs/`,
`dev_environment/**`, etc.). Keep existing check `if:` / skip combination from today’s partial snippet.

### D5: Pin action versions in docs

Use current major pins already proven in products (`actions/checkout@v7`, `dorny/paths-filter@v4`) in the recommended
snippet; products may bump independently.

## Risks / Trade-offs

- **[Risk] Reusable cancel races with caller cancel** → Mitigation: docs state reusable is complementary only; same PR
  group key shape reduces surprise
- **[Risk] Serialize release slows intentional parallel retries** → Mitigation: `cancel-in-progress: false` queues;
  group includes repository so other repos unaffected
- **[Risk] Path filter too narrow/wide** → Mitigation: suggested defaults + explicit “products may extend”

## Migration Plan

1. Land docs + reusable concurrency on the issue branch; draft PR `Fixes #76`.
2. Products adopt Feature-PR / release snippets via sibling issues when ready; bump `uses:` refs after merge.

## Open Questions

None — explore lock-ins applied.
