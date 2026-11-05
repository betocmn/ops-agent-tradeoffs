# Research brief

> How do token-efficiency incentives affect task success and policy compliance in AI agents performing high-volume back-office workflows?

This project will study whether efficiency incentives preserve, improve or worsen
reliability. The aim is reproducible evidence that can inform operational decisions,
support useful public technical work, and examine safety-relevant questions about
incentives and oversight. No results or novelty are claimed yet.

The initial domain is back-office operations in traditional industries, starting
with logistics. Shipment exceptions, carrier booking changes and reconciliation
are possible settings, not selected tasks. “High-volume” means recurring work where
small per-task differences can accumulate; it does not require a large benchmark
or distributed infrastructure. “Policy compliance” means adherence to explicit
business rules, permissions and approval requirements.

## Roles and current boundary

| Component | Role in later experiments |
| --- | --- |
| Environment | Holds business state, exposes permitted actions and records their effects. Harbor is the main environment and evaluation foundation. |
| Agent | Uses a model and a harness to choose and execute actions. Harbor's built-in Terminus 2 integration is the prospective harness; no agent is being implemented or vendored. |
| Verifier | Independently checks actual state changes and relevant actions against task requirements and business policies. |
| Evaluation | Runs specified conditions and aggregates outcomes, resource use and uncertainty. Inspect is separately available for future evaluation work; no Harbor–Inspect integration is planned for this milestone. |
| RL training | Updates model parameters using feedback from rollouts. It is a later intervention, distinct from measuring an existing model. |

This bootstrap installs tools and documents the research plan. It performs no
training, evaluations or model calls. It implements no tasks, simulated systems,
datasets, agents, integrations, rewards, verifiers, training loops or dashboards.
No task schema, reward formula, experiment size or first task has been chosen.

Only public material and, eventually, synthetic examples belong here. Real company
SOPs, customer records, private business information and production credentials
must remain outside this repository. This is an independent research project;
the documentation implies no company partnership or course affiliation.

## Principles for later experiments

- Measure task success and policy compliance separately. Verify actual state
  changes and relevant actions independently of the agent's completion claims.
- Measure unintended side effects, tokens, latency and inference cost as well as
  the requested outcome.
- Include failed attempts in cost accounting. Distinguish cost per attempted task
  from total spend per correct, compliant completion, including spend on failures
  and retries. Report when there are no such completions.
- Keep model inference costs separate from operational costs such as shipments
  or refunds.
- Use repeated runs and held-out cases before drawing conclusions; report
  uncertainty and failures alongside aggregate results.
- Distinguish inference-budget experiments, which change constraints at execution
  time, from changes to RL training rewards, which alter learning incentives.
- Comparisons between different models provide baselines but cannot isolate the
  causal effect of an efficiency incentive. A later causal RL study should use
  matched training conditions from the same base model while varying the incentive.

## Prospective training path

[Miles](https://miles.radixark.com/) is the prospective later RL training path,
with SGLang rollout support and multiple training backends. Miles, SGLang,
Megatron, PyTorch, model weights and GPU infrastructure are deferred until a
task is validated and a training budget exists.

## Literature review

A focused literature review remains a later milestone. Novelty is unverified
until that review compares questions, interventions, measurement methods and
limitations. No upstream benchmark or demo is run during bootstrap.

## Later milestones

1. Related-work review and selection of one bounded logistics workflow.
2. A synthetic environment and trustworthy verifier.
3. Baseline evaluations.
4. A bounded small-model RL experiment.
5. Held-out results, failure analysis and a reproducible write-up.
