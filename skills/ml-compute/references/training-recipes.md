# Training recipes: defaults, LR, LoRA vs full, and debugging

Defaults to start from, then change one thing at a time. Tune learning rate first; it
matters more than anything else in this file.

## Optimizer defaults

- **Custom PyTorch (Modal / local): AdamW** with betas (0.9, 0.95), weight decay 0.1, grad clip
  `clip_grad_norm_(params, 1.0)`, bf16 autocast, cosine or WSD schedule. β2=0.95 rather than the
  PyTorch default 0.999 because 0.999 remembers ~1000 steps, too slow for LLM loss landscapes.
  eps: 1e-8 is the usual value; autoresearch uses 1e-10 for bf16 (tiny second moments).
- **Don't weight-decay** embeddings, biases, norm parameters or per-layer scalars; do decay the
  2D weight matrices.
- **Memory pressure:** 8-bit Adam (bitsandbytes) saves ~30% of optimizer state memory at
  near-identical quality; Adafactor if that is still too much.
- **Muon** for 2D matrices plus AdamW for embeddings/head is a pretraining-from-scratch choice
  (autoresearch). For fine-tuning a pretrained model, stay with AdamW unless that's the experiment.
- **Tinker:** you pass `AdamParams(learning_rate=...)` to `optim_step`; the cookbook trainers
  handle the schedule (`lr_schedule`: `"linear"` (most common), `"cosine"`, `"constant"`).

## Learning rate by regime

| Regime | Starting LR | Where it comes from |
|---|---|---|
| Pretraining from scratch, ~100M-1B, AdamW | 3e-4, scaled down as width grows (`lr * (d_model/768)^-0.5`) | Orchestra recipes |
| Full fine-tune of a pretrained LM | 10-100x below pretraining LR (TRL SFT example: 2e-5) | Orchestra, TRL |
| LoRA SFT on Tinker, Qwen/Llama | `hyperparam_utils.get_lr(model)` = 5e-5 x 10 x (2000/hidden)^P (P=0.0775 Qwen, 0.781 Llama) | tinker-cookbook |
| LoRA SFT on Tinker, other families | `get_lr` raises; cookbook recipes use 2e-4 for SFT, so start there and sweep | tinker-cookbook |
| DPO | Tinker LoRA: 1e-5 with beta 0.1. TRL full-weight example: 5e-7 | both |
| RL (GRPO) | Tinker LoRA: 4e-5 math GRPO, 1e-5 multi-turn / RLHF. TRL: 5e-6 (safe) to 1e-5 | both |
| On-policy distillation, Tinker | 1e-4, LoRA rank 128 | tinker-cookbook |
| Reward model, Tinker LoRA | 3e-4 | tinker-cookbook RLHF recipe |

Rules of thumb:
- **LoRA wants ~10x the full fine-tune LR** (the cookbook fixes the multiplier at 10, after
  "LoRA Without Regret"). Reusing a full-FT LR on LoRA is a common reason a run "doesn't learn".
- **LR does not depend on LoRA rank** in the cookbook's experiments, so changing rank doesn't
  require re-tuning LR.
- **Batch size is a speed knob more than a quality knob.** When you change it, scale LR by about
  √(batch ratio); linear scaling works up to a point, then breaks.
- DPO and RL usually sit an order of magnitude below SFT, because big steps move the policy
  off the reference and destabilize it.
- Warmup 1-5% of steps; the decay phase (30-50% of training) matters more for final quality
  than warmup. Final LR 0 or ~10% of peak.

## LoRA vs full fine-tuning

- Start with **LoRA rank 32** (cookbook default). 8-16 for simple format/style changes; 64-128
  for harder tasks, big models, or distillation (the cookbook's distillation recipe uses 128).
- LoRA is usually enough for post-training (SFT, DPO, RL), costs far less memory, and forgets
  less. It's also the only option on Tinker.
- Go full fine-tune when a LoRA sweep over LR and rank plateaus below what the task needs, or
  when the change is large (new language, heavy continued pretraining). On Prime that means a
  `[deployment]` block; elsewhere it means Modal or a pod.
- Memory for full bf16 training with Adam: roughly 18-20 bytes x params before activations
  (a 1B model wants ~18-20 GB). QLoRA (4-bit base + adapters) is the cheap fallback.

## Debugging a run that isn't learning

Start with the data, not the hyperparameters. Formatting is the most common silent bug.
- **Decode 3-5 training examples back to text** and read them: special tokens, role markers,
  and the loss mask (on Tinker, check `TrainOnWhat` and print `weights`).
- **Renderer mismatch (Tinker):** get the name from
  `model_info.get_recommended_renderer_name(model)` instead of hard-coding it. High KL at step 0,
  before any update, points to a renderer problem. So does loss dropping while outputs look bad.
  Hybrid models need the `_disable_thinking` variant if you want no thinking block.
- **Overfit one batch.** If the loss can't go near zero on 1-8 examples, it's a bug, not tuning.
- **Stale sampler (Tinker):** after saving weights, make a new SamplingClient. An old one keeps
  sampling the old weights and gives no error.

| Symptom | Likely cause | Try |
|---|---|---|
| Flat loss from step 0 | LR far too low (often a full-FT LR on LoRA), schedule not applied, mask empty | print LR every step; check weights/mask; try 2-5x LR |
| Loss spike, then recovery or not | LR too high, a bad batch, fp16 overflow | 3-10x lower LR; clip at 1.0; roll back to the checkpoint before the spike and skip the batch |
| NaN | inf/NaN in inputs, fp16 without scaling, missing clip | check inputs; bf16; clip; lower LR; with grad accumulation, divide loss by accum steps |
| Slow upward drift | LR too high or data quality | lower LR; inspect the batches in the drift window |
| Train improves, eval doesn't | train/val leakage or mismatch, eval prompt format differs from training | check the split, template and decoding settings used at eval |
| OOM | batch or sequence too long | in order: smaller micro-batch + more grad accumulation; `PYTORCH_ALLOC_CONF=expandable_segments:True` (set before importing torch); activation checkpointing; 8-bit optimizer; LoRA/QLoRA |
| Tinker steps take minutes | sequential API calls | submit `forward_backward_async` and `optim_step_async` back to back, then await |

Watch gradient norm (a spike often comes before a loss spike), the LR actually applied, and
eval scores. Loss going down doesn't mean the task is improving; the eval does.

## First 10 minutes of a new run

1. Run 2-5 steps on the smallest model in the family (or locally) to catch import and config
   errors cheaply.
2. Print the resolved config: model id, renderer, LR, batch, LoRA rank, max length, log path.
3. Decode one batch and read it, mask included.
4. Log a baseline eval on the untrained model so the curve has a zero point.
5. Step 1: loss finite and in the expected range (≈ ln(vocab) for an untrained head; a
   pretrained LM on in-domain chat starts much lower). KL ≈ 0 if you log it.
6. Steps 5-10: loss moving, grad norm stable, logged LR matches the schedule, throughput (and
   tokens per step) as expected.
7. Read a few samples (RL: rollouts) before walking away.

Sources: Orchestra AI-Research-SKILLs 773a529, MIT (`10-optimization/ml-training-recipes/SKILL.md`,
`references/optimizers.md`, `experiment-loop.md`, `domain-specific.md`, `scaling-and-selection.md`;
`06-post-training/trl-fine-tuning/SKILL.md`, `grpo-rl-training/SKILL.md`); tinker-cookbook 1e53aa3
(`skills/research/SKILL.md`, `references/hyperparams.md`, `sft.md`, `preferences.md`, `distillation.md`,
`skills/debug/SKILL.md`, `tinker_cookbook/hyperparam_utils.py`).
