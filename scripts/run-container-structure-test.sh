#!/usr/bin/env bash
# Build a Docker image and run container-structure-test.
# Product repos override paths/tag via env (or positional args).
#
# Environment: host or Dev Container (needs Docker + container-structure-test on PATH).
#
# Usage:
#   ./scripts/run-container-structure-test.sh
#   CST_DOCKERFILE=docker/Dockerfile.api CST_IMAGE_TAG=myapp:test \
#     CST_CONFIG=docker/container-structure-tests/api.yaml \
#     ./scripts/run-container-structure-test.sh
#
# Positional (optional, override env):
#   $1 Dockerfile path
#   $2 image tag
#   $3 config file or directory of *.yaml tests

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}"

# shellcheck source=load-versions-env.sh
source "${SCRIPT_DIR}/load-versions-env.sh"

CST_DOCKERFILE="${1:-${CST_DOCKERFILE:-docker/Dockerfile}}"
CST_IMAGE_TAG="${2:-${CST_IMAGE_TAG:-app:structure-test}}"
CST_CONFIG="${3:-${CST_CONFIG:-docker/container-structure-tests}}"

if [[ ! -f "${CST_DOCKERFILE}" ]]; then
  echo "ERROR: Dockerfile not found: ${CST_DOCKERFILE}" >&2
  echo "Set CST_DOCKERFILE or pass path as \$1." >&2
  exit 1
fi

build_args=()
# Pass through common pins when present in versions.env (products may use more).
for var in PYTHON_VERSION UV_VERSION ALPINE_VERSION ALPINE_MINOR PIP_VERSION; do
  if [[ -n "${!var:-}" ]]; then
    build_args+=(--build-arg "${var}=${!var}")
  fi
done

echo "Building Docker image for container structure test (${CST_DOCKERFILE} → ${CST_IMAGE_TAG})..."
docker build -f "${CST_DOCKERFILE}" "${build_args[@]}" -t "${CST_IMAGE_TAG}" .

configs=()
if [[ -d "${CST_CONFIG}" ]]; then
  shopt -s nullglob
  configs=("${CST_CONFIG}"/*.yaml "${CST_CONFIG}"/*.yml)
  shopt -u nullglob
  if [[ ${#configs[@]} -eq 0 ]]; then
    echo "ERROR: no *.yaml / *.yml under ${CST_CONFIG}" >&2
    exit 1
  fi
elif [[ -f "${CST_CONFIG}" ]]; then
  configs=("${CST_CONFIG}")
else
  echo "ERROR: CST config not found: ${CST_CONFIG}" >&2
  echo "Set CST_CONFIG or pass path as \$3." >&2
  exit 1
fi

echo "Running Container Structure Test (${#configs[@]} config(s))..."
for cfg in "${configs[@]}"; do
  container-structure-test test --image "${CST_IMAGE_TAG}" --config "${cfg}"
done
