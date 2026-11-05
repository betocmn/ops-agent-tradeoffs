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
MODULES = {"harbor": "harbor", "inspect-ai": "inspect_ai", "pytest": "pytest", "ruff": "ruff"}


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
        LITELLM_LOCAL_MODEL_COST_MAP="True",
        PYTHON_DOTENV_DISABLED="1",
    )
    try:
        expected_python = (ROOT / ".python-version").read_text().strip()
        with (ROOT / "pyproject.toml").open("rb") as source:
            project = tomllib.load(source)
        requirements = project["project"]["dependencies"] + project["dependency-groups"]["dev"]
        versions = dict(requirement.split("==", 1) for requirement in requirements)
        if not MODULES.keys() <= versions.keys():
            raise ValueError("Required packages must have exact version pins")
    except (OSError, ValueError, KeyError, TypeError):
        print("ERROR: cannot read exact Python and dependency pins from repository configuration")
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

    docker_status()
    print("Installation: FAILED" if failures else "Installation: ready; no evaluation performed")
    return int(failures)


if __name__ == "__main__":
    sys.exit(main())
