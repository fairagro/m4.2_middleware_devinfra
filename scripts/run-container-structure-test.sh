#!/usr/bin/env bash
# Build a Docker image and run container-structure-test.
# Product repos override paths/tag via env (or positional args).
#
# Environment: host or Dev Container (needs Docker + container-structure-test on PATH).
#
# Usage (monolith Dockerfile — legacy / still valid until Bake adoption):
#   ./scripts/run-container-structure-test.sh
#   CST_DOCKERFILE=docker/Dockerfile.api CST_IMAGE_TAG=myapp:test \
#     CST_CONFIG=docker/container-structure-tests/api.yaml \
#     ./scripts/run-container-structure-test.sh
#
# Usage (Bake base + last stage — issue #36):
#   CST_BAKE_TARGET=api CST_IMAGE_TAG=myapp:test \
#     CST_CONFIG=docker/container-structure-tests/api.yaml \
#     ./scripts/run-container-structure-test.sh
#   Optional: CST_BAKE_FILE=docker-bake.hcl (default)
#
# Positional (optional, override env; ignored when CST_BAKE_TARGET is set):
#   $1 Dockerfile path
#   $2 image tag
#   $3 config file or directory of *.yaml tests

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}"

# Optional pins for Docker --build-arg / Bake *.args only. Do not use load-versions-env.sh
# (that enforces unrelated pins and rewrites .python-version).
VERSIONS_ENV="${REPO_ROOT}/versions.env"
if [[ -f "${VERSIONS_ENV}" ]]; then
  set -a
  # shellcheck source=/dev/null
  source "${VERSIONS_ENV}"
  set +a
fi

CST_DOCKERFILE="${1:-${CST_DOCKERFILE:-docker/Dockerfile}}"
CST_IMAGE_TAG="${2:-${CST_IMAGE_TAG:-app:structure-test}}"
CST_CONFIG="${3:-${CST_CONFIG:-docker/container-structure-tests}}"
CST_BAKE_TARGET="${CST_BAKE_TARGET:-}"
CST_BAKE_FILE="${CST_BAKE_FILE:-docker-bake.hcl}"

soft_skip_no_product_cst() {
  # Soft-skip shared Devinfra (and similar): no product app Dockerfile / CST suite.
  # Devinfra may still ship docker/Dockerfile.product-app.base + examples without a default
  # docker/Dockerfile or container-structure-tests/.
  if [[ ! -e "${REPO_ROOT}/docker" ]] \
    || {
      [[ ! -f "${REPO_ROOT}/docker/Dockerfile" ]] \
        && [[ ! -d "${REPO_ROOT}/docker/container-structure-tests" ]]
    }; then
    echo "WARNING: skipping container-structure-test ($1)." >&2
    exit 0
  fi
}

if [[ -n "${CST_BAKE_TARGET}" ]]; then
  if [[ ! -f "${CST_BAKE_FILE}" ]]; then
    soft_skip_no_product_cst "no ${CST_BAKE_FILE} for CST_BAKE_TARGET=${CST_BAKE_TARGET}"
    echo "ERROR: Bake file not found: ${CST_BAKE_FILE}" >&2
    echo "Set CST_BAKE_FILE or create repo-root docker-bake.hcl." >&2
    exit 1
  fi
else
  if [[ ! -f "${CST_DOCKERFILE}" ]]; then
    soft_skip_no_product_cst "no ${CST_DOCKERFILE}; no product CST layout under docker/"
    echo "ERROR: Dockerfile not found: ${CST_DOCKERFILE}" >&2
    echo "Set CST_DOCKERFILE or pass path as \$1 (or set CST_BAKE_TARGET for Bake)." >&2
    exit 1
  fi
fi

bake_set_args=()
build_args=()
# Pass through common pins when present in versions.env (products may use more).
for var in PYTHON_VERSION UV_VERSION ALPINE_VERSION ALPINE_MINOR PIP_VERSION; do
  if [[ -n "${!var:-}" ]]; then
    build_args+=(--build-arg "${var}=${!var}")
    bake_set_args+=(--set "*.args.${var}=${!var}")
  fi
done

if [[ -n "${CST_BAKE_TARGET}" ]]; then
  echo "Building Docker image via Bake (${CST_BAKE_FILE} target=${CST_BAKE_TARGET} → ${CST_IMAGE_TAG})..."
  docker buildx bake -f "${CST_BAKE_FILE}" "${CST_BAKE_TARGET}" --load \
    --set "${CST_BAKE_TARGET}.tags=${CST_IMAGE_TAG}" \
    "${bake_set_args[@]}"
else
  echo "Building Docker image for container structure test (${CST_DOCKERFILE} → ${CST_IMAGE_TAG})..."
  docker build -f "${CST_DOCKERFILE}" "${build_args[@]}" -t "${CST_IMAGE_TAG}" .
fi

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
