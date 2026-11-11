## Context

See `proposal.md` for motivation. After #350/#351, `docs/synced-paths.yaml` already keeps `.devcontainer/*` on
`python-product` and wires Infra as `foundation` + `gitops` + `infra-consumer`. Main specs still partially describe
Infra as “foundation only” in places; docs do not yet spell the Dev Container overlay / pin-ownership contract locked in
#352 explore.

## Goals / Non-Goals

**Goals:**

- Make the explore lock-in the durable contract (docs + OpenSpec + regression tests)
- Correct stale “Infra = foundation only” wording where this change already touches sync docs/specs
- Point at follow-ups #364 / API #670 for minikube→kind without implementing them

**Non-Goals:**

- Multi-stage Dockerfile / new gitops image target in Devinfra
- Syncing any `.devcontainer/**` to Infra
- Installing git-lfs or kind into the product image in this PR
- #354 Renovate on Infra; #353 actionlint; #151 `dev_environment/`

## Decisions

1. **Docs + specs + tests only (option A)** Rationale: acceptance is Propose / List / Explicit / never-ship; product
   image already correct on allowlist. Alternatives rejected: B (Dockerfile reshape) and C (stub gitops target) — churn
   without Infra adoption.

2. **Pin ownership is documentation (+ tests on allow paths), not a `versions.env` split** Rationale: file split belongs
   with #354 / later; #352 needs the ownership table readable now. git-lfs stays “shared-eligible” in docs while the
   existing shared-image rule (not a _required_ install) remains until a dedicated change installs it.

3. **minikube stays the documented product local-cluster tool today** Rationale: swap is #364; API smoke docs are API
   #670. Specs MUST NOT imply kind is already on the product image.

4. **Fix the Infra sync scenario wording while editing `product-repo-sync`** Rationale: “foundation only” is false after
   #351; updating that MODIFIED requirement avoids leaving a known lie next to the new Dev Container non-goals.

## Risks / Trade-offs

- [Docs drift vs #364] → Explicit “follow-up” language; link issues in docs.
- [Readers expect git-lfs installed because it is “shared-eligible”] → Keep the existing “not required on happy path”
  sentence next to the bucket table.
- [Over-specifying pins] → Buckets name exemplars (Helm / minikube / git-lfs / argocd / kind / ct), not every
  `versions.env` key.

## Migration Plan

1. Land docs + delta specs + tests on the issue branch; user commits; draft PR; archive syncs main specs.
2. No consumer migration in this PR. Infra unchanged. Products unchanged until #364 syncs.

## Open Questions

None for this MVP — adoption issue for a shared Infra image remains explicitly future work.
