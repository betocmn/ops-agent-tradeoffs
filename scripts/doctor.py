"""Check the local installation without running evaluations or exposing secrets."""

import importlib
import importlib.metadata
import os
import platform
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODULES = {
    "harbor": "harbor",
    "inspect-ai": "inspect_ai",
    "inspect-harbor": "inspect_harbor",
    "pytest": "pytest",
    "ruff": "ruff",
}


def inspect_harbor_status() -> bool:
    """Verify public exports and plugin registration without calling task factories."""
    try:
        bridge = importlib.import_module("inspect_harbor")
        for name in ("harbor", "harbor_scorer", "oracle"):
            if not callable(getattr(bridge, name, None)):
                print(f"ERROR: inspect_harbor.{name} is missing or not callable")
                return False
        entries = tuple(importlib.metadata.entry_points(group="inspect_ai", name="inspect_harbor"))
        if len(entries) != 1 or entries[0].value != "inspect_harbor._registry":
            print("ERROR: inspect_harbor Inspect plugin entry point is missing or incorrect")
            return False
        entries[0].load()
    except Exception as error:
        print(f"ERROR: Inspect Harbor plugin check failed ({type(error).__name__})")
        return False
    print("Inspect Harbor: public exports and Inspect plugin entry point verified")
    return True


def docker_status() -> None:
    """Inspect local Docker availability; never contact a remote daemon."""
    docker = shutil.which("docker")
    if docker is None:
        print("Docker CLI: unavailable; daemon: not checked (optional)")
        return
    print("Docker CLI: available")
    try:
        endpoint = os.environ.get("DOCKER_HOST", "")
        if os.environ.get("DOCKER_CONTEXT") or not endpoint:
            result = subprocess.run(
                [docker, "context", "inspect", "--format", "{{.Endpoints.docker.Host}}"],
                capture_output=True,
                text=True,
                timeout=5,
                check=True,
            )
            endpoint = result.stdout.strip()
        if not endpoint.startswith("unix://"):
            print("Docker daemon: remote or unknown endpoint; not probed (optional)")
            return
        environment = os.environ.copy()
        environment.pop("DOCKER_CONTEXT", None)
        result = subprocess.run(
            [docker, "--host", endpoint, "info", "--format", "{{.ServerVersion}}"],
            env=environment,
            capture_output=True,
            timeout=5,
            check=False,
        )
        status = "reachable" if result.returncode == 0 else "unreachable"
        print(f"Docker daemon: {status} (optional)")
    except (OSError, subprocess.SubprocessError, UnicodeError):
        print("Docker daemon: unavailable or timed out (optional)")


def main() -> int:
    os.environ.update(
        HARBOR_TELEMETRY="off",
        INSPECT_HARBOR_NO_TELEMETRY="1",
        HF_HUB_OFFLINE="1",
        LITELLM_LOCAL_MODEL_COST_MAP="True",
        PYTHON_DOTENV_DISABLED="1",
    )
    try:
        expected_python = (ROOT / ".python-version").read_text().strip()
        with (ROOT / "uv.lock").open("rb") as source:
            lock = tomllib.load(source)
        versions = {}
        for name in MODULES:
            matches = [entry["version"] for entry in lock["package"] if entry["name"] == name]
            if len(matches) != 1 or not isinstance(matches[0], str) or not matches[0]:
                raise ValueError("Required package lock record is missing or ambiguous")
            versions[name] = matches[0]
    except (OSError, ValueError, KeyError, TypeError):
        print("ERROR: cannot read exact Python and unambiguous dependency versions from uv.lock")
        return 1

    actual_python = platform.python_version()
    print(f"Python: {actual_python} (required: {expected_python})")
    failures = actual_python != expected_python
    for distribution, module in MODULES.items():
        try:
            version = importlib.metadata.version(distribution)
        except importlib.metadata.PackageNotFoundError:
            print(f"ERROR: {distribution} is not installed")
            failures = True
            continue
        print(f"{distribution}: {version} (required: {versions[distribution]})")
        failures |= version != versions[distribution]
        try:
            importlib.import_module(module)
        except Exception as error:
            print(f"ERROR: {module} import failed ({type(error).__name__})")
            failures = True

    failures |= not inspect_harbor_status()
    docker_status()
    print("Installation: FAILED" if failures else "Installation: ready; no evaluation performed")
    return int(failures)


if __name__ == "__main__":
    sys.exit(main())
