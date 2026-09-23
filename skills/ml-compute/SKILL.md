---
name: ml-compute
description: Choose where and how to run ML training and evaluation (Tinker, Prime Intellect Hosted Training, Modal, RunPod, local) and run it well - LoRA and full fine-tuning, RL post-training with verifiable rewards, custom losses, optimizer and LR defaults, debugging runs that do not learn, benchmark and calibration evals, and cost. Use when launching or planning any fine-tuning, RL, distillation, training or eval job, picking a GPU or service, estimating cost, or when a run diverges, collapses or stalls.
metadata:
  version: "1.0.0"
---

# ML Compute

Get the experiment onto the right machine, spend little, and learn from every run. The research method itself (hypothesis, verdict, log) is the `ml-research` skill; this one is the craft of running the job.

## Pick the route by what the experiment touches

- **Loss on hidden states, a new architecture, activations, anything custom:** Modal, or local while it fits. Tinker and Prime only see token logprobs and rewards.
- **RL on a task that exists, or can be written, as a verifiers environment:** Prime Hosted Training. You write a TOML file; rollouts, trainer and inference are hosted, and it reports real cost.
- **LoRA SFT, DPO, distillation, RL with your own Python loop or a custom logprob loss, on a model Tinker hosts:** Tinker. You write the loop; they run the GPUs.
- **Many hours on one dedicated box, a persistent disk, SSH:** RunPod (see the runpod skills).
- **First run of any new script:** local, tiny. A two-minute smoke run catches most bugs before paid compute does.

Details, limits and cost models: [routing](references/routing.md).

## Run it well

- Start small in every dimension that does not change the answer (model size, data, steps), and scale only a result that survived its checks.
- Read the first minutes of every run: loss at step 0 matches what the task implies, it falls, the gradient norm is sane, throughput is what you expected. [Training recipes](references/training-recipes.md) has LR and optimizer defaults and a triage for runs that spike, NaN, OOM or plateau.
- For RL, check the reward on hand-made good and bad examples before training, and watch reward, length and KL together; a rising reward alone is how reward hacking looks too. [RL post-training](references/rl-post-training.md).
- Keep the eval fixed and outside the code you change, and report calibration when the model outputs probabilities. [Evaluation](references/evaluation.md) covers lm-evaluation-harness and ECE/Brier.
- Put a number on cost before a long run; token-priced RL is dominated by rollouts.

## With a lab

When a lab is present (`labs.toml` above the working directory, or `lab` on PATH), use it rather than ad-hoc scripts:

- `lab templates` / `lab new exp <name> --template tinker-sft|prime-rl|modal-custom|interp` for a working starting point on each route.
- `lab run -H "hypothesis" -P "prediction" -- <cmd>` for every run; any script goes to a Modal GPU with `lab run -- modal run -m lab.modal_app --script train.py --gpu A10`.
- `lab bench <model> --tasks ...` records lm-eval accuracy with ECE, Brier and reliability figures; `lab fetch model|dataset <repo>[@rev]` pins downloads; `lab doctor` says which services are ready; `lab smoke` checks the templates still run.
- Log with `lab.log` / `lab.summary` / `lab.cost`, and figures with `lab.fig`, so runs stay comparable on `lab board`.

Service CLIs and SDKs change monthly. When a command or field in these references disagrees with the tool's own `--help` or source, trust the tool, and fix the reference.
