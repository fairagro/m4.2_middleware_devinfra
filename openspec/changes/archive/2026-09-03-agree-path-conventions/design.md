# Agree path conventions — Design

## Context

See proposal.md for motivation. Issue #3 exploration locked: per-product host tokens (not shared), volume naming pattern
B (slug table), doc at `docs/conventions.md`, tight scope (documentation only). Current consumer reality: API uses
`~/.config/middleware-api/tokens.env` and `middleware-api-bashhistory`; other repos use different volume short names;
all already use `middleware/` for packages.

## Goals / Non-Goals

**Goals:**

- Capture the locked conventions in `docs/conventions.md`
- Index from root README
- Give later extracts (#8 tokens, #10 Dev Container) a single written contract

**Non-Goals:**

- Implementing or moving `dev-tokens.sh` / wrappers (#8)
- Renaming existing Docker volumes or migrating host token files
- Changing product `devcontainer.json` overlays
- Expanding conventions beyond tokens, volumes, and package root

## Decisions

### 1. Per-product host token path (not shared)

- **Choice:** `~/.config/<product-slug>/tokens.env` per product
- **Alternatives:** Shared `~/.config/fairagro-m4.2/tokens.env`
- **Why:** Shared store couples Dev Containers on one machine in ways that are easy to forget; isolation is explicit.
  Cost (duplicate PAT prompts) accepted.

### 2. In-container token path stays universal

- **Choice:** `/commandhistory/tokens.env` in every Dev Container
- **Why:** Already used by the API helpers; lives on the _product-specific_ bashhistory volume, so isolation comes from
  the volume, not a different file path.

### 3. Volume naming pattern B — slug table

- **Choice:** Document `<product-slug>-bashhistory` / `<product-slug>-gh-config` with an explicit slug table
- **Alternatives:** Full repo dirname as volume name; leave undocumented
- **Why:** Readable short names matching current practice; sync templates parameterize `source=` via overlays

**Initial slug table:**

| Repository                     | product-slug           |
| ------------------------------ | ---------------------- |
| `m4.2_advanced_middleware_api` | `middleware-api`       |
| `m4.2_sql_to_arc`              | `sql-to-arc`           |
| `m4.2_middleware_harvester`    | `middleware-harvester` |
| `m4.2_middleware_devinfra`     | `middleware-devinfra`  |

### 4. Doc location `docs/conventions.md`

- **Choice:** Under `docs/`, linked from root README (issue said `CONVENTIONS.md`; house style after #2 is docs index)
- **Why:** Matches bootstrap docs pattern; keeps root README thin

### 5. Package root `middleware/`

- **Choice:** Document existing shared layout; Devinfra has none
- **Why:** Already true in all three products; no layout change required

## Risks / Trade-offs

- **[Risk] Slug table drifts from real volume names** → Mitigation: table reflects current names; renames are separate
  work; note “document now, migrate later”
- **[Trade-off] Per-product tokens mean repeated prompts** → Accepted for isolation
- **[Risk] Readers expect this change to rename volumes** → Mitigation: explicit non-goals in the doc intro

## Migration Plan

1. Add `docs/conventions.md` and README link only
2. No runtime or volume migration
3. Rollback = revert the doc commit
