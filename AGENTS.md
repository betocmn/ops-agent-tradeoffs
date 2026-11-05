# Repository instructions

## Scope

This is `ops-agent-tradeoffs`, a public research foundation for token efficiency,
task success and policy compliance in back-office agents. Keep the exact research
question in the README and research brief. Treat effects of efficiency incentives
neutrally; no first task, reward formula, task schema or experiment size is chosen.

The current milestone is installation and documentation only. Do not implement
tasks, environments, datasets, agents, tool integrations, rewards, verifiers,
training loops, dashboards or a Harbor–Inspect bridge. Harbor's built-in Terminus 2
is the prospective harness. Do not run model calls, upstream demos, evaluations,
paid services or training; do not download datasets/model weights or provision
GPUs/cloud sandboxes. Defer Miles, SGLang, Megatron and PyTorch until a validated
task and training budget. Read current official framework docs before using APIs.

## Commands and reproducibility

```bash
bash scripts/setup.sh
bash scripts/check.sh
.venv/bin/python scripts/doctor.py
.venv/bin/ruff format .
```

Setup uses pinned uv and managed Python 3.12 without changing system Python.
Routine setup and CI must use `uv sync --locked`; checks must work offline after
installation without credentials, Docker or GPUs. Keep direct pins, the uv pin
in `scripts/_common.sh`, `tool.uv.required-version`, `.python-version`, documentation
and `uv.lock` consistent when intentionally upgrading. Only an intentional
dependency update may regenerate the lock. Do not add cloud or training extras.

pytest is configured for future substantive tests in `tests/`; run
`.venv/bin/python -m pytest` once those exist. Do not add meaningless tests or
count an empty suite as validation. Installation checks establish readiness only.
Conductor uses `.conductor/settings.toml` and concurrent actions without ports.

## Data boundaries

Use public material and, eventually, synthetic examples only. Real company SOPs,
customer records, private business information and production credentials stay
outside this repository. Never print credentials. Keep `.env.example` blank and
tracked; keep secrets, local environments, caches, `.context`, raw logs, Harbor
jobs, trajectories, downloads and checkpoints ignored. Never commit session logs
or transcripts. Public writing must not imply partnerships, course affiliation,
completed research or verified novelty.

## Git conventions

Preserve existing work and the current branch. Follow a documented ticket prefix
only when a real user-supplied or roadmap ticket exists; never invent a ticket ID.
Use `origin/main` as the comparison and PR base. Do not push, release or change
repository visibility without authorization.

Auto-commit after completing each logical change and passing required checks.
Use semantic messages without parenthetical scopes, such as
`chore: bootstrap research workspace`. Use only the existing human Git identity.
Never add AI/LLM attribution, co-author trailers, product footers, signatures,
badges, generated-by notices or tool/model/provider names in commit messages or
branch/tag names. Do not add authorship attribution to PRs, comments or committed
artifacts. Required technical references are permitted. Inspect commit message
and author/committer metadata after every commit and remove prohibited attribution;
inspect PR title/body before any authorized publication.
