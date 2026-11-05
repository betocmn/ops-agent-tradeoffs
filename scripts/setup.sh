#!/usr/bin/env bash
set -euo pipefail
source "$(dirname -- "${BASH_SOURCE[0]}")/_common.sh"

if [[ ! -x "$UV" ]] || [[ "$("$UV" --version)" != "uv $UV_VERSION "* ]]; then
    command -v curl >/dev/null || { echo "Setup requires curl." >&2; exit 1; }
    mkdir -p "$REPO_ROOT/.context/tools/uv"
    installer="$(mktemp "$REPO_ROOT/.context/uv-installer.XXXXXX")"
    trap 'rm -f "$installer"' EXIT
    curl --fail --silent --show-error --location --retry 3 \
        "https://astral.sh/uv/$UV_VERSION/install.sh" -o "$installer"
    UV_UNMANAGED_INSTALL="$(dirname -- "$UV")" sh "$installer"
fi

require_uv
"$UV" --version
"$UV" python install "$(cat .python-version)" --no-bin
"$UV" sync --locked
echo "Setup complete. Run: bash scripts/check.sh"
