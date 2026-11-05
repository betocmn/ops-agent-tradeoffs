#!/usr/bin/env bash
set -euo pipefail
source "$(dirname -- "${BASH_SOURCE[0]}")/_common.sh"
require_uv

# Reconcile against the committed lock, without downloads or lock updates.
"$UV" sync --locked --offline --no-python-downloads
"$UV" pip check --offline
.venv/bin/ruff check .
.venv/bin/ruff format --check .

# The framework probes inherit no API keys; dotenv loading and telemetry are off.
probe() {
    env -i HOME="$HOME" PATH="$REPO_ROOT/.venv/bin:$PATH" \
        HARBOR_TELEMETRY=off LITELLM_LOCAL_MODEL_COST_MAP=True \
        INSPECT_HARBOR_NO_TELEMETRY=1 PYTHON_DOTENV_DISABLED=1 HF_HUB_OFFLINE=1 \
        "$@"
}

probe .venv/bin/python scripts/doctor.py
probe .venv/bin/harbor --help >/dev/null
echo "Harbor CLI help: OK"
probe .venv/bin/inspect --help >/dev/null
echo "Inspect CLI help: OK"
echo "Package and plugin installation checks passed. No task evaluation or training was run."
