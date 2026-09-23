# RL post-training: rewards, curves, and when not to use RL

## RL, SFT, DPO or distillation?

- **SFT** when you have good demonstrations. It's cheaper, steadier, and usually the first step
  anyway: RL and DPO work better from an SFT checkpoint than from a raw base model.
- **DPO** when you already have chosen/rejected pairs and no reliable scorer.
- **Distillation** when a stronger model already does the task. On-policy distillation (the
  student samples, the teacher scores it by per-token KL) gives dense signal per token, where RL
  gives one number per episode. Off-policy is plain SFT on teacher traces. On Prime, SFT
  distillation is `loss = "sft"` with a `[teacher]` block.
- **RL** when success can be checked (math answer, unit tests, a verifier, an environment) but
  good demonstrations are scarce, or when the model has to learn from its own mistakes
  (multi-turn tools, games). If the base model almost never succeeds, RL has nothing to
  reinforce: SFT or distill first.

## Designing the reward

- Prefer **verifiable outcome rewards** (exact answer, tests pass) over learned or judged ones.
  Every soft component is somewhere the policy can find a shortcut.
- Keep the **correctness term dominant** and shaping terms small. Tinker's `ProblemEnv` uses
  `format_coef * (check_format - 1) + check_answer` with `format_coef` 0.1: format only costs,
  correctness pays. The GRPO skill's example weights put correctness around 2.0 and format
  0.5-1.0.
- **Partial credit** (e.g. per-tag format points) helps a weak model find the format early, but
  it's the shaping most often hacked. Remove it or shrink it once format is learned. A staged
  run (format first, then correctness) is an option.
- A **length term** is usually a patch for another problem (see length exploitation below). If
  you need one, cap it rather than rewarding length linearly.
- Parse failures should get a defined reward (Tinker's `EnvFromMessageEnv` takes
  `failed_parse_reward`), not crash the episode or silently count as zero.

## Verify the reward before training

Most "RL doesn't work" runs are reward or parser bugs.
1. Run each reward function alone on 20-50 hand-picked completions: clearly right, clearly
   wrong, right answer in the wrong format, right format with a wrong answer, empty, truncated,
   and one with extra text after the answer. Check every score by hand.
2. Sample the untrained policy on ~100 prompts with the training settings (group size,
   temperature, max tokens) and look at the reward distribution. You want mixed groups. If
   nearly every group is all-0 or all-1 there is no gradient (advantages are centered within the
   group), so change the data difficulty or the model first.
3. Try to hack it yourself: a response that repeats the answer several times, hedges between
   candidates, or leaves the format empty. If a hack scores well, the policy will find it.
4. For a learned reward model, check held-out pairwise accuracy (chosen scored above rejected;
   the TRL reference aims for >80%) before using it as a reward.

## Reading the curves

| Signal | Healthy | Worry when |
|---|---|---|
| Mean reward (`env/all/reward/total` on Tinker, `reward` in TRL) | rising, noisy | flat from step 0 (reward bug, LR too low, no mixed groups); rising while eval falls (hacking) |
| Share of mixed groups (`by_group/frac_mixed`; also `frac_all_good`, `frac_all_bad`) | a solid fraction | toward 0: no signal left. All-good means the data is too easy, all-bad too hard |
| Within-group reward std (TRL `reward_std`) | stays above ~0.1 | toward 0: groups are identical, collapse |
| KL between the sampling and training policy (Tinker `optim/kl_sample_train_v1`/`v2`); TRL `kl` is to the reference | small; the cookbook says RL is stable when KL < 0.01 | jumping or climbing steadily: lower the LR |
| Entropy (Tinker `optim/entropy`) | declines slowly | falls off a cliff: collapse |
| Response length | moves with the task | grows steadily while accuracy is flat: length exploitation |
| Held-out eval | follows reward | diverges from reward: overfitting or hacking |

Read the samples, not just the numbers: on Tinker the `*_rollout_summaries.jsonl` and
`*_logtree.json` files; on Prime `prime train rollouts <run_id> --step N`. A glance at 5-10 rollouts
every few dozen steps catches hacking long before the metrics do. Judge from more than one
run, since single RL runs are noisy.

## Failure modes

- **Reward hacking:** reward rises but held-out accuracy or a manual read doesn't. Typical cases:
  a parser that accepts the answer anywhere in the text (the cookbook's toy `check_answer` does
  substring matching, which rewards listing many candidates), format points without content,
  a judge that favors confidence or length. Fix the reward, then restart from a checkpoint taken
  before the hacking began.
- **Collapse:** group std, mixed-group share and entropy all go to zero, and samples become
  near-identical. Lower the LR, raise the group size, check that sampling temperature is 1.0
  (the Tinker RL default), or add or raise a KL penalty.
- **Length exploitation:** length climbs while accuracy stalls, often through repetition or
  padding a thinking block, and truncation at `max_tokens` becomes common. Check the length and
  truncation rates, cap `max_tokens`, give truncated episodes a defined reward (Tinker reports
  `response_hit_length_limit`), and consider Prime's `repetition` / `gibberish` pre-batch filters.

## Knobs

- **Group size** (Tinker `group_size`, TRL `num_generations`, Prime `rollouts_per_example`):
  more rollouts give a better advantage estimate and more mixed groups on hard prompts, at
  proportional sampling cost. Starting points: 4 for plumbing tests, 8 as a default (Prime and
  the GRPO skill), 16 for math (the cookbook GSM8K recipe uses batch 128 x group 16).
- **Batch** (`groups_per_batch` / `batch_size`) is prompts per step. Debug at 4 x 2 on Tinker
  (`groups_per_batch=4, group_size=2`), then scale.
- **KL penalty:** Tinker `kl_penalty_coef` defaults to 0.0 in RL (`kl_reference_config` sets the
  reference). Many verifiable-reward runs keep it off and control drift with the LR. Add it when
  outputs drift in style, or when a soft or learned reward invites hacking. TRL PPO uses
  `kl_coef` 0.05-0.2. For TRL GRPO's KL coefficient, check the current `GRPOConfig` docs.
- **Constant-reward groups:** Tinker `remove_constant_reward_groups` (default False) and Prime's
  `zero_advantage` filter drop groups with no signal.
- **Off-policy steps:** Tinker `num_substeps > 1` needs the `ppo` loss and a lower LR. With
  `AsyncConfig(max_steps_off_policy=...)` rollouts can lag the policy; keep the lag small.
- **LR:** see `training-recipes.md`. RL runs well below SFT.

Sources: Orchestra AI-Research-SKILLs 773a529, MIT (`06-post-training/grpo-rl-training/SKILL.md`,
`README.md`, `examples/reward_functions_library.py`; `06-post-training/trl-fine-tuning/SKILL.md`,
`references/online-rl.md`, `reward-modeling.md`, `dpo-variants.md`); tinker-cookbook 1e53aa3
(`skills/research/SKILL.md`, `references/rl.md`, `hyperparams.md`, `distillation.md`, `preferences.md`,
`tinker_cookbook/rl/train.py`, `rl/metrics.py`, `rl/metric_util.py`, `rl/data_processing.py`);
prime-cli 9073f2e (`commands/rl.py`).
