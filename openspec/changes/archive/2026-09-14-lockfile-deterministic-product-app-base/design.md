## Context

See proposal.md — Why. Today `package-builder` already copies `pyproject.toml`, `uv.lock`, and `middleware/` and builds
wheels; `binary-builder` only receives wheels and runs `uv pip install --system /tmp/wheels/*.whl`. Final product images
copy from `export-binaries` / last stage — intermediate builder size does not affect runtime image size.

## Goals / Non-Goals

**Goals:**

- Transitive runtime deps in `binary-builder` come from `uv.lock` (`--frozen` / no live resolve for those deps).
- Preserve wheel → `PYINSTALLER_IMPORT` / `PYINSTALLER_ENTRY` → `pyinstaller --onedir` flow.
- Keep `PYINSTALLER_VERSION` from `versions.env`.
- Document the contract in `docs/ci.md`.

**Non-Goals:**

- Option B (`uv export` requirements-only) or Option C (full source `uv sync` instead of wheels).
- Changing Bake HCL / last-stage layout / ARG names beyond what Option A needs.
- Running product Bake smoke inside Devinfra CST (no product app image here).
- Locking PyInstaller via `uv.lock` (stays versions.env).

## Decisions

1. **Option A** — Copy lock + workspace metadata from `package-builder` (or build context) into `binary-builder`;
   `uv sync --frozen` for dependencies (workspace members not installed from source / `--no-install-workspace` or
   equivalent), then `uv pip install --system --no-deps /tmp/wheels/*.whl`, then pin-install PyInstaller. **Alternative
   B** rejected for this change: equivalent determinism, but A keeps a single lock artifact without an export step.
   Builder layer size is acceptable (not in runtime image).

2. **System / venv** — Prefer the existing `--system` (or `UV_SYSTEM_PYTHON`) style already used so PyInstaller still
   sees packages on the image Python; if `uv sync` defaults to `.venv`, either sync into system Python with documented
   flags or put `.venv/bin` on `PATH` for the pyinstaller invocation — pick the smallest change that keeps entry
   resolution working. Exact flags land in apply; contract is “locked deps + wheels `--no-deps`”.

3. **Docs** — State in `docs/ci.md` that binary-builder must not resolve wheel `Requires-Dist` from the live index;
   lockfile is SoT for transitive deps.

## Risks / Trade-offs

- **[Risk] `uv sync --frozen` needs full workspace pyprojects** → Copy the same tree `package-builder` already has
  (`pyproject.toml`, `uv.lock`, `middleware/`), or copy from that stage.
- **[Risk] Extra packages from lock vs wheel-only install** → Use `--no-dev` / no extra groups; only install what the
  locked runtime graph needs for the built packages.
- **[Risk] PyInstaller / entry import breaks if env layout changes** → Verify `python -c import …` path still works;
  adjust PATH or `--system` accordingly in apply.

## Migration Plan

1. Land Dockerfile + docs + spec in Devinfra; sync.
2. Products rebuild Bake; open smoke follow-ups if needed.
3. Rollback: revert base Dockerfile to previous `uv pip install` without `--no-deps` / lock sync.

## Open Questions

- None for MVP (system vs `.venv` is an apply detail under Decision 2).
