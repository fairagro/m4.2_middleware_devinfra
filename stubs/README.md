# Product-local type stubs (optional)

Shared incomplete stubs for `arctrl` / `fable_library` were **removed**. Untyped
third-party imports are handled without a full API mirror:

- **mypy** (`mypy.ini`): `[mypy-arctrl*]`, `[mypy-fable_library*]` with
  `ignore_missing_imports = True` — **mypy is the type gate** (hooks + CI)
- **Call sites:** `# type: ignore[import-untyped]` on `arctrl` / `fable_library`
  imports when needed (same pattern as other untyped deps)
- **basedpyright / Pylance** (`pyrightconfig.json`): `typeCheckingMode: "off"` —
  keep the language server (goto, rename, hover, completions); do **not** emit a
  second set of type diagnostics in the IDE. Do **not** add fleet-wide
  `reportAny` / `reportUnknown*Type` silences.

Incomplete `__getattr__ -> Any` stubs did not improve type safety; maintaining
them was busywork.

## What may still live under `stubs/`

| Stub / silence | Where | Why |
| --- | --- | --- |
| `owslib/`, `rdflib/`, other product libs | Product-local only | High churn / not shared fleet-wide |
| One-off libs (`lxml`, `defusedxml`, …) | `# type: ignore[import-untyped]` on the import | Few call sites |

Products MAY keep a `stubs/` directory for product-local packages and point
`stubPath` at it. Do **not** reintroduce shared `arctrl` / `fable_library` stub
trees unless they carry **real** symbol types worth maintaining.

Do **not** patch per-module third-party silences into product `pyproject.toml`
when the synced `mypy.ini` / `pyrightconfig.json` already cover the fleet packages.
