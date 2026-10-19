#!/usr/bin/env bash
# Soft-load MYPYPATH / PYLINT_SOURCE_ROOTS from a product env file (file wins).
# Only those keys are read (no full `source` of the file). Missing file = no-op.
# Re-applies on every invoke so product.env edits beat stale Compose env_file snapshots.
#
# Usage:
#   source scripts/load-quality-path-env.sh [path-to-env-file]
# Default file: .devcontainer/product.env (relative to repo root / cwd when sourced).
# Callers that need process/workflow overrides MUST apply them AFTER sourcing this helper.

_load_quality_path_env() {
  local env_file="${1:-.devcontainer/product.env}"
  local line key val

  if [[ ! -f "${env_file}" ]]; then
    return 0
  fi

  while IFS= read -r line || [[ -n "${line}" ]]; do
    # trim CR; skip blank/comments
    line="${line%$'\r'}"
    [[ -z "${line}" || "${line}" =~ ^[[:space:]]*# ]] && continue
    [[ "${line}" =~ ^[[:space:]]*(MYPYPATH|PYLINT_SOURCE_ROOTS)[[:space:]]*=(.*)$ ]] || continue
    key="${BASH_REMATCH[1]}"
    val="${BASH_REMATCH[2]}"
    # strip optional surrounding quotes
    if [[ "${val}" =~ ^\"(.*)\"$ ]]; then
      val="${BASH_REMATCH[1]}"
    elif [[ "${val}" =~ ^\'(.*)\'$ ]]; then
      val="${BASH_REMATCH[1]}"
    fi
    # file wins over process/container snapshot (every invoke)
    export "${key}=${val}"
  done <"${env_file}"
}

# When executed (not sourced), print exports for debugging / CI eval.
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  set -euo pipefail
  _load_quality_path_env "${1:-.devcontainer/product.env}"
  printf 'MYPYPATH=%s\n' "${MYPYPATH-}"
  printf 'PYLINT_SOURCE_ROOTS=%s\n' "${PYLINT_SOURCE_ROOTS-}"
else
  _load_quality_path_env "${1:-.devcontainer/product.env}"
fi
