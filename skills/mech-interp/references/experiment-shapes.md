# Experiment shapes: an interp campaign in the lab

Commands come from `~/src/labs/README.md`; read it for anything not covered here. The research
loop itself (hypothesis, cheapest test, keep/revert, log) is the ml-research skill's; what an
interp claim needs as evidence is the ml-research evidence standard
(`~/src/skills/skills/ml-research/references/mech-interp.md`). This file is about the plumbing.

## Set up

```bash
lab new campaign j48-subspace --metric vs_random --goal max --budget 40 \
    --question "Does the top-8 J(4→8) subspace of GPT-2 carry next-token prediction?"
cd campaigns/j48-subspace
lab new exp jac --template interp && cd experiments/jac
```

The `interp` template (`~/src/labs/src/lab/templates/interp/`) already builds J over prompts, ablates the
top k after block `src`, compares with random bases (and optionally SAE features), and logs three
figures plus `summary(loss_increase, vs_random, sigma_ratio_k)`. Start there and change the
question, not the scaffolding.

## What goes in `locked/`

`locked/` is hashed on the first run; a later change is recorded (`lock.ok = false`) and warned
about, and `lab lock --accept "why"` starts a new comparison epoch. Put anything the verdict
depends on there:
- `eval.txt`: evaluation texts, one per line. The template reads it via `LAB_LOCKED_DIR`.
- The prompt set used to build J or to choose directions (for example `prompts.txt`). The
  template builds J on `DEFAULT_PROMPTS` and measures on `eval.txt`, falling back to a separate
  `DEFAULT_EVAL`; keep your own two sets disjoint the same way, and write `eval.txt` before the
  first run so the measurement is hashed from run one.
- Patching pairs (for example `pairs.jsonl` with clean, corrupt, answer, counterfactual answer),
  token-aligned and checked once with the target tokenizer.
- A held-out split you do not look at until the claim is written down.
Model name and revision belong in the run arguments; record the resolved revision in the run.

## Metric and goal

The campaign metric should be one number that already contains its control, so runs compare
across seeds and settings:
- Subspace ablation: `vs_random` = loss increase of the chosen basis minus mean loss increase
  of random bases of the same k, `goal = "max"` (the template's setting). Raw `loss_increase`
  is worth logging but not optimising: it rises with k and with removed norm.
- Patching: fraction of logit difference restored, (m − m_corrupt)/(m_clean − m_corrupt),
  averaged over held-out pairs, `goal = "max"`.
- Steering: target effect at a fixed collateral budget (for example loss increase on
  unrelated text ≤ 0.05 nats), `goal = "max"`, so scale cannot buy the win.
Set `noise_floor` in `campaign.toml` from measured spread, for example twice the std of
`vs_random` across random-basis seeds, so deltas inside it read as inconclusive on the board.

Write the prediction before the run: `lab run -H "..." -P "vs_random > 0.1" -- ...`. Judge
with `lab verdict r003 keep|revert|inconclusive|failed -m "why"`; `keep` makes it the baseline.

## Figures (`from lab import fig`)

Each call writes a JSON spec into the run; outside `lab run` it only returns the spec.
- Spectra: `fig.line({"trained": S/S[0], "random-init": S0/S0[0]}, x=idx, log_y=True,
  mark_x=(k + 0.5, f"top {k} ablated"), x_label="singular index", title=..., sub=...)`.
  A random-init series on the same axes is the quickest read of how much is learned.
- Bases vs controls: `fig.dots(items, x_label="next-token loss increase",
  reference=(rand_mean, "random", rand_std), title=...)`, where items are
  `{"label", "mean", "lo", "hi", "highlight"?}`; bootstrap CIs from `interp.bootstrap`, random
  bases as min–max over seeds. Add PCA-top-k and SAE-top-k rows when you have them.
- Per-token projections: `fig.tokens([(label, words, values)], value_label="projection",
  title=...)`; diverging by default, so signed projections read directly. Use it to show where
  a direction is read and to spot position-0 or punctuation artefacts.
- Patching grids: `fig.heatmap(grid, x=tokens, y=[str(l) for l in layers], diverging=True,
  value_label="restored", title=...)`; `annotate=(row, col, "label")` marks the cell you name.
- Linearisation checks and steering sweeps: `fig.line` of effect against ε or alpha, with the
  linear prediction or the random-direction control as a second series.
Other types exist (`scatter`, `hist`, `bars`, `reliability`, `multiples`, `table`); see
`~/src/labs/src/lab/fig.py` for their arguments.

## Fast loop, then scale

Iterate on a small model locally, where a full J is seconds to minutes (GPT-2 small, d = 768):

```bash
lab run -H "Top-8 J(4→8) directions matter more than random" -P "vs_random > 0.1" -- \
  uv run --with torch --with transformers python experiment.py --model gpt2 --src 4 --dst 8 --k 8
```

Scale when the small-model result is stable across seeds and prompt sets, and the question is
whether it holds at size. Modal ships the experiment folder, `locked/` and `lib/`, installs the
experiment's `requirements.txt`, and brings metrics, figures and artifacts back into the run:

```bash
lab run -H "..." -P "..." -- modal run -m lab.modal_app --script experiment.py \
  --args "--model Qwen/Qwen3-8B --src 14 --dst 24 --vectorize" --gpu A100-80GB
```

- Modal time is billed to your Modal account and not recorded as cost; `budget_usd` counts
  only amounts a service reports.
- At d = 4096 a full J is 4096 VJPs per prompt. `--vectorize` batches them if memory allows;
  otherwise use the randomised top-k method in `jacobian-subspaces.md`.
- Big outputs (saved Jacobians, activation dumps) go on the `lab-data` volume at `/data`, not
  into artifacts.
- Gated models (Llama, Gemma) need Hugging Face auth inside the container; `lab/modal_app.py`
  does not wire a secret as of this reading, so check before launching one.
- The default Modal timeout is 6 hours (`timeout_hours` in `modal_app.main`).

## Campaign shape that tends to work

1. One small-model run with the template as is: does the spectrum have a knee, and does the
   top-k basis beat random at all?
2. Controls before variants: removed-norm and PCA bases, random-init spectrum, held-out texts.
3. Sweep k and (src, dst) as separate runs branched with `lab new exp <name> --from r00N`.
4. Only then the causal story: patching or steering along the basis (`interventions.md`).
5. Scale the one or two surviving claims; write them in `findings.md` under
   "What we believe now", with run ids.

Sources: Orchestra AI-Research-SKILLs 773a529 (MIT): transformer-lens/references/tutorials.md (patching heatmap shape); lab `README.md`, `src/lab/templates/interp/{README.md,experiment.py}`, `src/lab/fig.py`, `src/lab/modal_app.py`, `src/lab/cli.py`.
