# Path conventions

Shared naming and path conventions for the three m4.2 product repos and this Devinfra repo. Later extracts (tokens
helpers, Dev Container sync, quality scripts) MUST follow these rules.

This document is **documentation only**. It does not rename existing Docker volumes or migrate host token files.

Issue: [#3](https://github.com/fairagro/m4.2_middleware_devinfra/issues/3).

## Product slugs

Short slugs identify a product in **Docker volume names**:

| Repository                     | product-slug           |
| ------------------------------ | ---------------------- |
| `m4.2_advanced_middleware_api` | `middleware-api`       |
| `m4.2_sql_to_arc`              | `sql-to-arc`           |
| `m4.2_middleware_harvester`    | `middleware-harvester` |
| `m4.2_middleware_devinfra`     | `middleware-devinfra`  |

## Personal tokens

Personal developer tokens (e.g. `GH_TOKEN`, `GITGUARDIAN_API_KEY`) are **per-product**, not shared across Dev Containers
on the same machine.

| Environment        | Path                                   |
| ------------------ | -------------------------------------- |
| Dev Container      | `/commandhistory/tokens.env`           |
| Host (local clone) | `~/.config/<git-repo-name>/tokens.env` |

The in-container path is the same string everywhere; isolation comes from each product's own bashhistory volume. On the
host, `<git-repo-name>` is the GitHub repository name from `origin` (e.g. `m4.2_middleware_devinfra`) — not the short
product-slug and not a `PRODUCT_SLUG` env var. Do **not** use a shared directory such as `~/.config/fairagro-m4.2/`.

## Docker volumes

Named volumes follow:

- `<product-slug>-bashhistory` → mount at `/commandhistory`
- `<product-slug>-gh-config` → mount at `/home/vscode/.config/gh` (when used)

Product `devcontainer.json` overlays own the `source=` names. Shared Devinfra files MUST NOT hardcode another product's
volume name. Renaming existing volumes is out of scope for this conventions doc (migrate later if needed).

## Package root

Product application packages live under a repo-relative `middleware/` tree:

```text
middleware/<package>/
```

Shared quality tooling and pre-commit hooks MAY target `middleware/` as a whole. This Devinfra repository has **no**
product `middleware/` packages.
