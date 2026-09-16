# Shared type stubs (arctrl / fable_library)

Keep third-party silence **out of** synced `mypy.ini` (Devinfra sync overwrites it).

## Why stubs exist (and what they are not)

Incomplete stubs here use `__getattr__ -> Any` so **mypy** can import untyped
third-party packages (`arctrl`, `fable_library`) without:

- `[mypy-arctrl*]` / similar overrides in synced `mypy.ini`, or
- scattering `# type: ignore[import-untyped]` on every call site across products.

That is the advantage over “drop stubs and silence everything”: **one synced stub
tree** keeps mypy green in all products without polluting the shared mypy config or
hundreds of import lines.

These stubs are **not** a full typed model of arctrl. Do **not** expand them into a
hand-maintained API mirror just to please basedpyright.

## basedpyright / `reportAny`

Because symbols resolve through `__getattr__ -> Any`, basedpyright would otherwise
emit `Type of "ARC" is Any` (`reportAny`) on normal imports. Synced
[`pyrightconfig.json`](../pyrightconfig.json) sets `"reportAny": "none"` so incomplete
stubs stay viable without that noise.

Alternative considered and rejected for the shared baseline: delete stubs and silence
missing-type / import-untyped diagnostics per tool (mypy ignores, pyright
`reportMissingTypeStubs`, etc.). That reintroduces either synced `mypy.ini` module
overrides or per-import ignores — the problem stubs were introduced to avoid
([#64](https://github.com/fairagro/m4.2_middleware_devinfra/issues/64),
[#67](https://github.com/fairagro/m4.2_middleware_devinfra/issues/67)).

Products MUST append `stubs` to `MYPYPATH` in hooks/CI; basedpyright uses
`stubPath: "stubs"` in synced `pyrightconfig.json`.

## What belongs where

| Stub / silence                         | Where                                                                                            | Why                                 |
| -------------------------------------- | ------------------------------------------------------------------------------------------------ | ----------------------------------- |
| `arctrl/`, `fable_library/`            | This tree → product sync ([#67](https://github.com/fairagro/m4.2_middleware_devinfra/issues/67)) | Shared across middleware products   |
| `owslib/`, `rdflib/`                   | Product-local only                                                                               | Many import sites / multi-module    |
| One-off libs (`lxml`, `defusedxml`, …) | `# type: ignore[import-untyped]` on the import                                                   | Few call sites — stubs not worth it |

Do **not** use `# type: ignore[import-untyped]` for packages covered by the shared stubs above after sync. Do **not**
patch per-module `[mypy-…]` overrides into synced `mypy.ini`.
