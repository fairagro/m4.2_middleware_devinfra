# Product-local type stubs (optional)

Shared incomplete stubs for `arctrl` / `fable_library` were **removed**. Untyped
third-party imports are silenced in synced tool config instead:

- **mypy** (`mypy.ini`): `[mypy-arctrl*]`, `[mypy-fable_library*]` with
  `ignore_missing_imports = True`
- **basedpyright** (`pyrightconfig.json`): `reportMissingTypeStubs = "none"`,
  `useLibraryCodeForTypes = false`, and `reportAny = "none"` so untyped libraries
  (no `py.typed`) are not deep-analyzed into noisy errors / `Any` import warnings

Incomplete `__getattr__ -> Any` stubs did not improve type safety over those
silences; maintaining them was busywork.

## What may still live under `stubs/`

| Stub / silence                         | Where              | Why                              |
| -------------------------------------- | ------------------ | -------------------------------- |
| `owslib/`, `rdflib/`, other product libs | Product-local only | High churn / not shared fleet-wide |
| One-off libs (`lxml`, `defusedxml`, …) | `# type: ignore[import-untyped]` on the import | Few call sites |

Products MAY keep a `stubs/` directory for product-local packages and point
`stubPath` at it. Do **not** reintroduce shared `arctrl` / `fable_library` stub
trees unless they carry **real** symbol types worth maintaining.

Do **not** patch per-module third-party silences into product `pyproject.toml`
when the synced `mypy.ini` / `pyrightconfig.json` already cover the fleet packages.
