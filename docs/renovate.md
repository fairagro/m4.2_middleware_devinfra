# Renovate (shared dependency updates)

Canonical Renovate config and GitHub workflow live in this Devinfra repo and are intended for sync into the three m4.2
product repos ([#13](https://github.com/fairagro/m4.2_middleware_devinfra/issues/13)).

| Artifact                                                              | Role                              |
| --------------------------------------------------------------------- | --------------------------------- |
| [`renovate.json`](../renovate.json)                                   | Shared Renovate config (SoT)      |
| [`.github/workflows/renovate.yml`](../.github/workflows/renovate.yml) | Per-repo self-hosted Renovate job |

**Do not** hand-edit these after sync in product checkouts — see
[`docs/synced-paths.global.md`](synced-paths.global.md).

## GitHub Actions secret: `RENOVATE_TOKEN`

The workflow does **not** use SOPS and does **not** rely on `GITHUB_TOKEN` alone. Create a **repository** Actions secret
named `RENOVATE_TOKEN` in each repo that runs the workflow (Devinfra + each product after adoption).

Use a fine-grained PAT (or equivalent) with at least: Contents (R/W), Pull requests (R/W), Metadata (R); Workflows /
Issues (R/W) as required by your Renovate setup (same pattern as the API repo README).

Until the secret exists, scheduled runs fail; after setting it, use **Actions → Renovate → Run workflow**.

## Local CLI dry-run

The Dev Container pins the **Renovate npm CLI** via `RENOVATE_VERSION` in [`versions.env`](../versions.env) (`renovate`
on `PATH`). That pin is for local dry-runs only. CI runs
[`renovatebot/github-action`](../.github/workflows/renovate.yml) at its own Action version (currently `v46.2.6`) — keep
the Action major aware of the CLI major when bumping either pin; they are not the same artifact.

From the repo root (no PR creation):

```bash
renovate --version
# Config / dependency discovery only (adjust flags to your Renovate major as needed):
LOG_LEVEL=debug renovate --platform=local --dry-run=full
```

Use a GitHub token in the environment when the dry-run must query GitHub datasources (`GITHUB_COM_TOKEN` /
`RENOVATE_TOKEN`). Prefer the personal-token helpers for interactive `gh` work; Renovate’s bot PAT is separate from
developer `GH_TOKEN` when you use a dedicated automation user.

## Dependabot migration (products)

| Keep                                                                                    | Drop / avoid                                                                            |
| --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| **Dependabot alerts** (Security tab) — Renovate can read vulnerability alerts on GitHub | **Dependabot version updates** (`.github/dependabot.yml`)                               |
| Prefer **Renovate** for dependency update PRs                                           | Running Dependabot version updates **and** Renovate as general updaters (duplicate PRs) |

Optional: turn off Dependabot **security update** PRs if Renovate owns security updates, so only one bot opens fix PRs.
Keep alerts enabled.

## Adoption / sync (#13)

1. Land config + workflow here; set `RENOVATE_TOKEN` on Devinfra; smoke-test with `workflow_dispatch`.
2. Sync `renovate.json` and `.github/workflows/renovate.yml` into API / sql-to-arc / harvester.
3. Set `RENOVATE_TOKEN` per product repo; remove Dependabot version-update config; converge API onto the shared config
   (drop divergent local rules unless documented as a thin overlay / `extends`).

Reusable `reusable-renovate.yml` is **out of scope** for now — the thin workflow is expected to stay identical across
repos via sync.
