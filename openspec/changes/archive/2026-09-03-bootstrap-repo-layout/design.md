## Context

See proposal.md for motivation. Today the repo already has a working step-0 `.devcontainer/` (Dockerfile, compose, `devcontainer.json`), `versions.env`, `.python-version`, and `scripts/` helpers, plus a narrative `.devcontainer/README.md` that currently acts as the front door. Issue #2 asks for documented layout before later extracts; exploration decided root README + growing `docs/` is the presentation model, with `.gitkeep` stubs for empty shared dirs.

## Goals / Non-Goals

**Goals:**

- Establish root README as the only front door (purpose, ownership, versions blurb, docs index)
- Move Dev Container operator content to `docs/devcontainer.md` and delete `.devcontainer/README.md`
- Land empty shared-path dirs so later epic issues have stable homes
- Document `versions.env` / `.python-version` without claiming product-wide sync is already done

**Non-Goals:**

- Path conventions for tokens/volumes/package-root (#3)
- Extracting skills, policy, quality scripts, or CI
- Expanding the Dev Container toolchain (#10)
- Sync automation (#13)
- Initializing product OpenSpec trees here
- Changing image build behavior, pins, or scripts beyond deleting the misplaced README

## Decisions

### 1. Delete `.devcontainer/README.md` entirely (no stub pointer)

- **Choice:** Remove the file; discovery is via root README → `docs/devcontainer.md`
- **Alternatives:** Keep a one-line pointer in `.devcontainer/README.md`
- **Why:** User preference; avoids a second, drifting entry point next to files that consumers will later overlay

### 2. Single bootstrap feature doc: `docs/devcontainer.md`

- **Choice:** Only real doc at bootstrap; other dirs empty with `.gitkeep`
- **Alternatives:** Also add `docs/versions.md` now
- **Why:** Versioning is mostly exercised through the Dev Container today; a short root blurb + detail section in `docs/devcontainer.md` is enough until CI/quality consumers of the pins appear

### 3. Root README stays thin; docs grow

- **Choice:** Purpose + ownership + versions note + bullet links to `docs/*`
- **Alternatives:** Fat README that embeds operator guides
- **Why:** Matches the agreed long-term pattern; epic work adds docs and index links rather than bloating the README

### 4. `.gitkeep` for empty dirs

- **Choice:** `.agents/skills/.gitkeep`, `.cursor/.gitkeep`, `.github/.gitkeep`
- **Alternatives:** Per-dir PURPOSE.md stubs citing filling issues
- **Why:** User preference; minimal noise. `docs/` will contain `devcontainer.md` so no `.gitkeep` required there unless we want one for consistency (not required)

### 5. Framing of early Dev Container content

- **Choice:** Keep existing tooling files; rewrite docs to describe current operator reality and note that full product-shared toolchain still lands with #10
- **Alternatives:** Strip or revert Dev Container until #10
- **Why:** Useful now for developing this repo; honest about sequencing without undoing working setup

### 6. Versioning wording

- **Choice:** Call out `versions.env` as pin SSOT and `.python-version` as aligned Python pin; detail edit → rebuild / postCreate sync in `docs/devcontainer.md`
- **Why:** User asked for visibility of the global versioning system without inventing #3/#10 sync claims

## Risks / Trade-offs

- **[Risk] Empty `.github/` / `.cursor/` look unfinished** → Mitigation: root README states they are reserved for later shared extracts; epic #1 is the roadmap
- **[Risk] Product repos still have fat `.devcontainer/README.md` until sync** → Mitigation: acceptable until #10/#13; this change only fixes the canonical repo
- **[Risk] Volume names in docs (`middleware-devinfra-*`) may change in #3** → Mitigation: document current names; #3 updates conventions and docs together
- **[Trade-off] Versioning detail lives under Dev Container doc** → Acceptable until a non-container consumer of pins needs its own doc

## Migration Plan

1. Add root README, `docs/devcontainer.md`, and `.gitkeep` skeleton in one PR implementing this change
2. Delete `.devcontainer/README.md` in the same PR
3. No runtime migration; no consumer sync yet
4. Rollback = revert the PR (docs/layout only)
