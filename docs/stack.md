# Stack and installation boundary

Official documentation reviewed on 2026-11-05. Installed versions appear in the
[README](../README.md); `pyproject.toml` declares constraints and `uv.lock` fixes
exact versions. Only the base `harbor`, `inspect-ai` and `inspect-harbor`
distributions are requested, without cloud or training extras. Some provider SDKs
are mandatory transitive dependencies; installing them does not configure or
exercise providers.

## Installed foundation

- **Python 3.12 and uv:** a dependency-only project (`tool.uv.package = false`),
  without a build backend, package or application entry points. The shared script
  helper pins uv; `tool.uv.required-version` enforces the same release. Setup uses
  the versioned official installer with `UV_UNMANAGED_INSTALL`, provisions the
  exact `.python-version` using `uv python install --no-bin`, then runs
  `uv sync --locked`. Tool binaries, managed Python and the uv cache stay under
  `.context/`; dependencies stay in `.venv/`. System Python and shell profiles
  are untouched. See [uv project configuration](https://docs.astral.sh/uv/concepts/projects/config/),
  [installer options](https://docs.astral.sh/uv/reference/installer/), and
  [locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/).
- **Harbor:** the canonical task format and native path for task development,
  validation and experiments. Its built-in `terminus-2` integration is the
  prospective native harness; no agent is vendored or implemented here.
  Actual jobs will need a selected execution environment; local Docker is a
  future option, not an installation prerequisite. See
  [installation](https://docs.harborframework.com/getting-started/installation)
  and [pre-integrated agents](https://docs.harborframework.com/agents/pre-integrated-agents).
- **Inspect:** our intended primary runner for evaluation suites, checkpoint
  comparisons, structured logs and analysis. See the
  [official guide](https://inspect.aisi.org.uk/).
- **inspect-harbor 1.0.0:** loads Harbor-format tasks for execution by Inspect.
  Added with the workspace's pinned uv using `uv add "inspect-harbor>=1.0"`;
  it was the only added package, with no existing dependency upgrades. Version
  1.0 no longer depends on the `harbor` distribution; we retain Harbor for its
  native execution path. See the [official integration guide](https://meridianlabs-ai.github.io/inspect_harbor/)
  and our [architecture](architecture.md) for task sharing, harness differences,
  current compatibility limits and a future local-task example.
- **pytest and Ruff:** development dependencies. Ruff checks existing code;
  pytest is configured for later substantive tests and is not run against an
  empty suite as evidence of readiness.

`scripts/check.sh` uses `uv sync --locked --offline --no-python-downloads` and
`uv pip check --offline`, then runs local checks. Required dependency, import or
CLI failures fail the command. The doctor checks versions against the lock and
imports `inspect_harbor` plus the public `harbor`, `harbor_scorer` and `oracle`
exports. It discovers the installed `inspect_ai` entry point named
`inspect_harbor`, verifies its `inspect_harbor._registry` target and loads the
plugin module. No factory is invoked, task loaded, verifier run or sandbox created.
It also reports optional Docker CLI/local daemon availability; remote contexts
are not contacted.
Framework probes use a clean environment without API credentials, disable dotenv
loading, and use LiteLLM's bundled model cost map. `HARBOR_TELEMETRY=off` disables
[Harbor's default telemetry](https://docs.harborframework.com/telemetry/telemetry).
`INSPECT_HARBOR_NO_TELEMETRY=1` disables the bridge's
[Hub download reporting](https://meridianlabs-ai.github.io/inspect_harbor/advanced.html#hub-download-counts).
These checks verify package and plugin installation only. No task has been
evaluated end to end and no provider or experimental architecture is validated.

## Deferred training

[Miles](https://miles.radixark.com/) is a prospective later training path.
Miles, SGLang, Megatron, PyTorch, model downloads and GPU/cloud infrastructure
are not installed or provisioned here. Revisit them after task validation and
an explicit training budget. This bootstrap performs no training.

## Conductor and CI

[`.conductor/settings.toml`](../.conductor/settings.toml) uses the current
[repository settings schema](https://conductor.build/schemas/settings.repo.schema.json):
setup invokes `bash scripts/setup.sh`, and the check action invokes
`bash scripts/check.sh`. Concurrent execution is appropriate because workspaces
use their own files and no shared services. No legacy `conductor.json` or
`CONDUCTOR_PORT` is needed. The scripts resolve the repository root and work in
non-interactive shells. The Mac app reads shared settings from the remote default
branch; cloud setup reads the workspace's creation branch. Settings are prepared
here but are not published by this bootstrap.

Linux CI calls the same pinned setup twice and the same check script on
`ubuntu-24.04`, without secrets or services, and checks that `uv.lock` is unchanged.
Local verification does not imply that a remote workflow has run; no commits are
pushed during this milestone.
