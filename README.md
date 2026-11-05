# Token Efficiency and Reliability in Back-Office Agents

> How do token-efficiency incentives affect task success and policy compliance in AI agents performing high-volume back-office workflows?

`ops-agent-tradeoffs` is an independent research project on incentives and
oversight in recurring operational work, starting with logistics. Efficiency
incentives could preserve, improve or worsen success and compliance. Policy
compliance means following explicit business rules, permissions and approval
requirements. High volume means small per-task differences can accumulate; it
does not require a large benchmark or distributed infrastructure now.

The aim is reproducible evidence for operational decisions and useful public
technical work. Shipment exceptions, carrier booking changes and reconciliation
are possible settings; the first task has not been chosen. No results, company
partnerships or course affiliation are claimed.

## Current capabilities

This milestone provides a locked Python environment, installation checks,
Conductor actions, Linux CI and a research plan. Harbor is the primary environment
and evaluation foundation, with its built-in Terminus 2 integration as the
prospective agent harness. Inspect is installed separately for future evaluations.

There are no tasks, simulated systems, datasets, agents, tool integrations,
rewards, verifiers, training loops, dashboards or Harbor–Inspect integration.
Installation readiness does not establish end-to-end evaluation capability.

## Setup and checks

On macOS or a normal Linux workspace, with Bash, curl, CA certificates and
network access for installation:

```bash
bash scripts/setup.sh
bash scripts/check.sh
```

Setup installs uv **0.13.7** in `.context/tools/uv`, provisions Python **3.12.16**
in `.context/python`, and runs `uv sync --locked` to populate `.venv`. It is
idempotent and needs no system Python changes, shell profile edits, virtual
environment activation, Docker daemon, GPU or API keys. CI uses the same scripts
and repeats setup to check idempotency. Keep `.context` while using this environment;
rerun setup if its tools or caches are removed.

Checks synchronize offline from the committed lock, check dependency consistency,
run Ruff lint and formatting checks, import the required packages, exercise
`harbor --help` and `inspect --help`, and run the doctor. Framework probes receive
no API credentials; dotenv loading and Harbor telemetry are disabled. Docker
availability is informational. No external service is needed after installation.

Other local commands, from the repository root:

```bash
.venv/bin/python scripts/doctor.py
.venv/bin/ruff check .
.venv/bin/ruff format --check .
```

pytest is installed and configured for future substantive tests under `tests/`.
When those tests exist, run `.venv/bin/python -m pytest`. The bootstrap has no
test suite and does not count an empty suite as validation.

| Component | Pinned version |
| --- | --- |
| Python | 3.12.16 |
| uv | 0.13.7 |
| Harbor | 0.25.0 |
| Inspect (`inspect-ai`) | 0.3.287 |
| pytest | 9.2.0 |
| Ruff | 0.17.3 |

The dependency-only project has no distributable package or application API.
`uv.lock` records transitive dependencies. See [stack notes](docs/stack.md) for
official references, the deferred training path and Conductor settings.

## Research and data boundaries

Read the [research brief](docs/research-brief.md) for measurement principles,
the planned literature review and later milestones. `tasks/` and `evals/` contain
placeholders only.

Use only public material and, eventually, synthetic examples. Keep real company
SOPs, customer records, private business information and production credentials
outside this repository. `.env.example` documents the credential boundary;
setup and checks do not need credentials or load `.env` files.

This bootstrap performs no model calls, evaluations, upstream demos, sandbox
provisioning, dataset or model-weight downloads, or training. Miles, SGLang,
Megatron, PyTorch and GPU infrastructure remain deferred until a validated task
and training budget exist.
