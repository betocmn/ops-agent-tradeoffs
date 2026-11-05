#!/usr/bin/env bash
# Sourced by setup/check; all paths belong to this workspace.
REPO_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

UV_VERSION="0.13.7"
UV="$REPO_ROOT/.context/tools/uv/uv"
export UV_CACHE_DIR="$REPO_ROOT/.context/uv-cache"
export UV_PYTHON_INSTALL_DIR="$REPO_ROOT/.context/python"
export UV_PROJECT_ENVIRONMENT="$REPO_ROOT/.venv"
export UV_PYTHON_PREFERENCE=only-managed
export UV_NO_ENV_FILE=1
export UV_NO_PROGRESS=1

require_uv() {
    if [[ ! -x "$UV" ]] || [[ "$("$UV" --version)" != "uv $UV_VERSION "* ]]; then
        echo "Pinned uv $UV_VERSION is missing; run bash scripts/setup.sh." >&2
        exit 1
    fi
}
