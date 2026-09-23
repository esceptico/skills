# Routing: which service for which job

Pick by what the experiment has to touch, then by cost. The lab records the run either way
(`lab run -- <cmd>`), and each route has a template: `tinker-sft`, `prime-rl`, `modal-custom`, `interp`.

## Quick decision

1. **Need hidden states, activations, a new architecture, or a loss on anything other than
   token logprobs?** Modal (`modal-custom` or `interp`), or local if it fits. Tinker and Prime
   only expose the policy's token logprobs and rewards.
2. **RL on a task that already exists (or can be written) as a verifiers environment?**
   Prime Hosted Training usually wins: you write a TOML file and the rollouts, trainer and
   inference are hosted.
3. **LoRA SFT, DPO, distillation, or RL with your own Python env or custom logprob loss, on a
   model in Tinker's lineup?** Tinker (`tinker-sft`). You write the loop; they run the GPUs.
4. **A single run that needs a dedicated GPU box for many hours or days** (big full fine-tune,
   long pretraining, data you want sitting on a disk)? RunPod or a Prime pod.
5. **Small model, short debug loop, CPU-bound eval?** Local. Usually the first stop for any new
   script, because a 2-minute local smoke test catches most bugs before paid compute.

## What each can and cannot do

| | Tinker | Prime Hosted Training | Modal | RunPod / pods | Local |
|---|---|---|---|---|---|
| Training type | LoRA only (`create_lora_training_client`) | LoRA on shared clusters; full fine-tune on a dedicated cluster with a `[deployment]` block or `--full-finetune` | anything | anything | anything that fits |
| Methods | SFT, RL (GRPO-style, `importance_sampling` / `ppo` / `cispo` / `dro`), DPO, RLHF, on/off-policy distillation | `loss = "rl"` or `"sft"` (SFT distillation from a teacher); OPD "not yet supported on hosted runtimes" | your code | your code | your code |
| Models | hosted lineup only (Qwen3.x, Nemotron, gpt-oss, DeepSeek-V3.1, Kimi-K2.6, GLM-5.3, Inkling) | whatever `prime train models` lists | any HF / custom | any | small |
| Custom loss | `forward_backward_custom`: any differentiable loss over token logprobs | no; reward lives in the environment | yes | yes | yes |
| Hidden states / arch changes | no | no | yes | yes | yes |
| Environment / data | your Python env classes, run client-side | verifiers env pushed to the Environments Hub | your code | your code | your code |
| Output | `tinker://` checkpoints; download adapter or merge to HF | hosted checkpoints and adapters | your files (write to a Volume) | your disk | your disk |

Details worth knowing before you route:
- **Tinker** LoRA flags: `train_mlp`, `train_attn`, `train_unembed` on the training client.
  The lab's `tinker-sft` template notes that `loss_fn_inputs` carries only `target_tokens` and
  `weights`, so extra per-token signals must be folded into weights. Check the exact model id
  with `service_client.get_server_capabilities().supported_models`; some are only served with a
  suffix (e.g. `zai-org/GLM-5.3:peft:262144`). Retired models can't train or sample any more.
- **Prime** config (`prime train init` writes a template): `model`, `loss`, `max_steps`
  (default 100), `batch_size` (128), `rollouts_per_example` (8), optional `learning_rate`
  (template comment: default 1e-4), `lora_alpha`, `[sampling] max_tokens`, `[[env]] id`, optional
  `[eval]`, `[val]`, `[[pre_batch_filters]]` (`zero_advantage`, `gibberish`, `repetition`),
  `[checkpoints]`, `[teacher]`. The model table caption says all LoRA models support 64K context.
  Launch with `prime train rl.toml`; `prime rl` is a deprecated alias.
- **Modal** fits anything custom and is billed per second, so bursty sweeps are cheap. Long jobs
  need checkpoints on a Volume (the lab mounts `lab-data` at `/data`) and a `timeout` set;
  check Modal's current maximum function timeout before planning a multi-day run.
- **RunPod** suits long dedicated runs where a persistent disk and SSH matter more than
  per-second billing. Use the runpod skills for provisioning. Prime also rents pods
  (`prime availability list`, `prime pods create`).

## Cost models

| Service | Billed by | Where to read the price | In the lab's budget |
|---|---|---|---|
| Tinker | per model, by tokens; cost tier tracks active parameters for MoE | tinker-docs.thinkingmachines.ai/tinker/models/ | no: `tinker-sft` records tokens, the bill is your account's |
| Prime Hosted Training | per 1M tokens, separate Input, Output and Train columns | `prime train models` | yes: `prime-rl` records the total from `prime train usage <run_id>` |
| Modal | per GPU-second while the container runs | modal.com/pricing | no: your Modal bill |
| RunPod | per hour while the pod exists, including idle time | runpod.io pricing | no: your RunPod bill |
| Local | electricity and your time | n/a | no |

The lab records only amounts a service reports, so the campaign budget caps Prime spend and
anything your code passes to `cost()`; read prices on the day rather than from notes like this one.

Cost reasoning that usually holds:
- RL cost on token-priced services is dominated by rollouts:
  `steps x batch_size x rollouts_per_example x (prompt + completion tokens)`. Check the live price in
  `prime train models` before raising `max_steps`, `rollouts_per_example` or `max_tokens`.
- On Tinker and Prime you pay for tokens, not wall time. Modal bills while a container is up
  (keep-warm included); a pod bills until you stop it, so pods pay off only when the GPU stays busy.
- Budget the smoke test: a few steps on the smallest model in the family first, because config
  errors are the most common way to burn money.

## When the route is wrong

- You need an activation-level metric mid-way through a Tinker run: move that experiment to
  Modal with an open-weights model of similar size, rather than approximating with logprobs.
- The Prime env doesn't exist and writing a verifiers env is more work than the experiment:
  Tinker's `ProblemEnv` / `MessageEnv` in plain Python is usually faster to stand up.
- A Modal run keeps hitting its timeout: checkpoint and resume, or move to a pod.

Sources: tinker-cookbook 1e53aa3 (`skills/research/SKILL.md`, `references/sdk.md`, `models.md`,
`hyperparams.md`, `README.md`, `AGENTS.md`); prime-cli 9073f2e (`commands/rl.py`, `commands/usage.py`,
`main.py`, `README.md`); Orchestra AI-Research-SKILLs 773a529, MIT (`09-infrastructure/modal/SKILL.md`);
labs `README.md`, `templates/*/README.md`, `src/lab/modal_app.py`.
