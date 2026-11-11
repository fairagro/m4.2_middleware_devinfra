#!/usr/bin/env bash
# Thin kubeconform wrapper for consumer CI after helm template (or any rendered manifests).
# Usage:
#   scripts/run-kubeconform.sh [kubeconform flags…] [--] [manifest files…]
#   helm template … | scripts/run-kubeconform.sh [kubeconform flags…]
# Does not discover charts, does not run helm template, does not ship CRD schema packs.
# Environment: host or Dev Container. Pin: versions.env KUBECONFORM_VERSION (+ install-kubeconform.sh).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

pin=""
if [[ -f "${REPO_ROOT}/versions.env" ]]; then
  pin="$(grep -E '^KUBECONFORM_VERSION=' "${REPO_ROOT}/versions.env" | tail -n1 | cut -d= -f2- || true)"
fi

if ! command -v kubeconform >/dev/null 2>&1; then
  echo "run-kubeconform: kubeconform is not on PATH." >&2
  echo "run-kubeconform: use the Linux Dev Container (KUBECONFORM_VERSION=${pin:-unset}) or bash scripts/install-kubeconform.sh." >&2
  exit 1
fi

echo "run-kubeconform: using $(command -v kubeconform) pin=${pin:-unset}" >&2

# No file args and stdin is a TTY → show usage (kubeconform alone may hang waiting for stdin).
if [[ $# -eq 0 && -t 0 ]]; then
  echo "run-kubeconform: pass manifest files and/or pipe YAML on stdin; extra args are forwarded to kubeconform." >&2
  echo "run-kubeconform: example: helm template ci ./charts/app | bash scripts/run-kubeconform.sh -summary" >&2
  exit 1
fi

exec kubeconform "$@"
