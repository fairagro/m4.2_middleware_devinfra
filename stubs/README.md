# Product-local type stubs (optional)

Shared incomplete stubs for `arctrl` / `fable_library` were **removed**. Untyped fleet imports are silenced in **synced
tool config** (prefer config over call-site ignores):

| Tool                                              | Fleet silence for `arctrl` / `fable_library`                                                            |
| ------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| **mypy** (`mypy.ini`)                             | `[mypy-arctrl*]` / `[mypy-fable_library*]` `ignore_missing_imports = True` — **type gate** (hooks + CI) |
| **pylint** (`.pylintrc`)                          | `ignored-modules=arctrl,fable_library` (import-error / member analysis)                                 |
| **ruff** (`ruff.toml`)                            | No missing-import diagnostics for third-party packages; `known-third-party` for isort only              |
| **basedpyright / Pylance** (`pyrightconfig.json`) | `typeCheckingMode: "off"` — language server only; type gate remains mypy                                |

Do **not** add `# type: ignore[import-untyped]` on `arctrl` / `fable_library` imports for the fleet default — the
fragments above cover hooks/CI. Other one-off untyped libs (few call sites) MAY still use per-import ignores when no
config silence exists.

Incomplete `__getattr__ -> Any` stubs did not improve type safety; maintaining them was busywork.

## What may still live under `stubs/`

| Stub / silence                           | Where                                          | Why                                |
| ---------------------------------------- | ---------------------------------------------- | ---------------------------------- |
| `owslib/`, `rdflib/`, other product libs | Product-local only                             | High churn / not shared fleet-wide |
| One-off libs (`lxml`, `defusedxml`, …)   | `# type: ignore[import-untyped]` on the import | Few call sites                     |

Products MAY keep a `stubs/` directory for product-local packages and point `stubPath` at it. Do **not** reintroduce
shared `arctrl` / `fable_library` stub trees unless they carry **real** symbol types worth maintaining.

Do **not** patch per-module third-party silences into product `pyproject.toml` when the synced fragments already cover
the fleet packages.
