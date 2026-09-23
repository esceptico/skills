# Evaluation: harness runs, calibration, and keeping the eval fixed

A number is only comparable when the model is the only thing that changed between runs. Most
of this file is about holding everything else still.

## lm-evaluation-harness essentials

```bash
pip install lm-eval
lm_eval --tasks list                                   # exact task names

# HF model (add ,peft=<adapter dir or repo> to evaluate a LoRA adapter on top of the base)
lm_eval --model hf \
  --model_args pretrained=<model>,dtype=bfloat16 \
  --tasks gsm8k,arc_challenge --num_fewshot 5 \
  --batch_size auto --output_path results/<run> --log_samples

# vLLM backend, usually several times faster for generation-heavy tasks
lm_eval --model vllm \
  --model_args pretrained=<model>,tensor_parallel_size=1,dtype=auto,gpu_memory_utilization=0.8 \
  --tasks gsm8k --batch_size auto

# Any OpenAI-compatible server (vLLM serve, TGI, llama.cpp, Ollama)
lm_eval --model local-completions \
  --model_args model=<name>,base_url=http://localhost:8000/v1,num_concurrent=1 \
  --tasks gsm8k

# Your own task: YAML in a folder; check it loads, then run 5 examples
lm_eval --tasks my_task --include_path my_tasks/ --limit 0
lm_eval --model hf --model_args pretrained=<model> --tasks my_task --include_path my_tasks/ --limit 5 --log_samples
```

The upstream docs also show a `lm-eval run ...` subcommand form. Use whichever the installed
version accepts.

Flags that change the number, so record them with every result:
- `--num_fewshot`: 0-shot and 5-shot numbers are different experiments. Published results
  mostly give the few-shot setting per task; match it when you compare against a paper.
- `--apply_chat_template` and `--fewshot_as_multiturn`: instruct and chat models usually need
  the chat template; without it a chat model sees raw text and underperforms. Some tasks
  (e.g. `gsm8k_cot_llama`) only reproduce reported numbers with both flags. Base models are
  usually run without the template. Keep the choice the same across every run you compare.
- `--system_instruction`: a system prompt is part of the eval.
- `--gen_kwargs temperature=0,...`: set decoding explicitly. For sampled evals set `--seed`
  (and the seed in vLLM's `model_args`) and report mean ± std over several seeds.
- `--limit N`: for smoke tests only. A limited run isn't comparable to a full one.
- Batch size and dtype rarely matter much, but record them. Quantized loading (`load_in_4bit`)
  can move scores, so don't compare a 4-bit eval with a bf16 one.
- Chat-only APIs can't run loglikelihood (multiple-choice) tasks, only generation tasks.

Metric names differ by task: `acc`, `acc_norm` (length-normalized; HellaSwag-style tasks usually
report this one), `exact_match`. Each comes with a `_stderr`. Treat differences within about
2 stderr as noise. The lab's `noise_floor` should be at least that wide.

## Pitfalls

- **Prompt format drift** is the most common reason "the same eval" moves: a different template,
  few-shot count, system prompt, answer-extraction regex, or the generation length limit. Exact 0% on a
  generation task almost always means extraction failed. Read `--log_samples` output before
  believing any surprising number.
- **Thinking models:** strip the reasoning block before extraction (on OpenAI-compatible
  backends the harness takes a `think_end_token` in `model_args`), and give enough generation
  budget. Otherwise you are grading truncated thoughts.
- **Train/eval format mismatch:** evaluate with the same renderer/template the model was trained
  on. On Tinker, the cookbook's benchmark framework (`run_benchmarks`, `BenchmarkEvaluator`)
  uses the training renderer and `BenchmarkConfig.for_model(model)` defaults.
- **Contamination:** before trusting a big gain, search the training data for eval items (exact
  and near-duplicate matches on the question text). A fine-tune that beats much larger models
  everywhere is a red flag. For your own evals, keep the held-out split away from the data
  pipeline from the start.
- **Checking the setup:** reproduce one published baseline number before measuring your own
  model, since it catches setup errors.

## Calibration metrics

Given confidence p_i for the predicted answer and correctness y_i ∈ {0,1}:
- **Brier score** = mean((p_i − y_i)²). A proper scoring rule: lower is better, and it rewards
  both calibration and sharpness. It's usually the best single number for a campaign metric,
  because it has no binning choices. For multi-class, sum over classes.
- **ECE** = Σ_b (n_b / N) · |acc_b − conf_b| over confidence bins b. Easy to read, but it depends
  on the number of bins and on equal-width vs equal-mass binning. Fix those in the locked eval
  and report them. With few samples per bin it's noisy, so bootstrap a CI. A constant predictor
  at the base rate can score ECE ≈ 0, so report it next to accuracy or Brier, not alone.
- **Reliability diagram:** accuracy vs confidence per bin, with bin counts shown. It shows over-
  vs under-confidence, which one scalar hides. In the lab: `fig.reliability({"base": (conf0,
  correct0), "trained": (conf1, correct1)}, title=...)`.
- Where confidence comes from is part of the eval: token probability of the answer, a verbalized
  number, or agreement across samples. Changing the source changes the metric.
- Temperature scaling on a held-out split is the standard post-hoc fix. Fit it on validation
  data, never on the test split.

## Keeping the eval fixed

In the lab the eval lives in the campaign's `locked/` folder (data, prompts, extraction code,
metric code). It is hashed on the first run, and a later change is recorded and warned about.
`lab lock --accept "why"` starts a new comparison epoch. That covers the files, so the rest is
up to you:
- Put everything that defines the number in `locked/`: eval data, prompt template, few-shot
  examples and their order, extraction regex, bin count, decoding settings. Keep the lm-eval task
  YAML there too and point `--include_path` at it.
- Pin versions (lm-eval, transformers, vLLM) in the experiment's requirements, because harness
  updates can change task prompts.
- Evaluate the base model once per epoch as the zero point, with the same settings.
- If the eval has to change (a bug in extraction, say), accept a new epoch and re-run the
  baseline, rather than comparing across the change.
- Use a separate dev split for iterating on prompts and hyperparameters, so the locked test
  split isn't slowly overfit by many small choices.

Sources: Orchestra AI-Research-SKILLs 773a529, MIT (`11-evaluation/lm-evaluation-harness/SKILL.md`,
`references/api-evaluation.md`, `custom-tasks.md`, `benchmark-guide.md`, `distributed-eval.md`);
EleutherAI lm-evaluation-harness docs via Context7 (`README.md`, `docs/interface.md`,
`docs/python-api.md`, `tasks/gsm8k/README.md`, read 2026-09-23) for `--apply_chat_template`,
`--fewshot_as_multiturn`, `--system_instruction`, `--seed`, `peft=`, `think_end_token`;
tinker-cookbook 1e53aa3 (`skills/research/SKILL.md`, `references/ops.md`); labs `README.md`.
