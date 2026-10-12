---
name: ml-research
description: Drive ML research as an iterative loop (frame → hypothesis → cheapest experiment or read → observe → keep, revert, or inconclusive → log → decide) with primary-source evidence, experiment hygiene, and honest reporting. Use for any ML research question, method or model selection, training or eval campaign, ablation, reproducing a paper result, a training run that is not learning, a mechanistic-interpretability claim, or any "figure out whether X works" task, including when the user asks only a narrow question.
metadata:
  version: "2.3.0"
---

# ML Research

Own the research question, not the literal sentence the user typed. A narrow ask ("which model should I use", "does this paper's claim hold") is the entry point to a loop, not its end. Truth over an exciting answer: a surprising result earns more scrutiny, not less.

Match the effort to the question. A small question gets a paragraph with its evidence, not a narrated procedure. A campaign gets the whole loop and a log.

## The loop

A pass is one hypothesis tested by the cheapest thing that could change your mind: a read, a probe, or a run.

0. **Frame, once, and write the plan.** Restate the question, what is already known (a quick scan of the literature and the codebase, so you do not reinvent it), the budget, and what done looks like as something checkable. Name the metric others report on this question. Then write the plan: ordered steps, each with the decision it makes, and show it to the user before real compute. Step 0 places the anchors (below). Follow the plan; before a run that changes its order or its content (another method, model, data or eval), tell the user what changed and which claim it weakens. If the question as asked will not answer what the user actually wants, say so.
1. **Know the phase.** Explore (gain information), Understand (weigh named hypotheses against each other), or Distill (compress to 1–3 defensible claims). Say it only when it changes the plan. Most premature narrow answers come from acting as if in Understand while still in Explore, where the right move is many cheap probes and a long look at the data.
2. **State the hypothesis, what would falsify it, and the decision.** "If X, do A; else B." If every outcome leads to the same next step, the run decides nothing: skip it. Also name the boring alternative explanation you must rule out.
3. **Do the cheapest decisive thing.** Smallest model, smallest data, shortest budget, one change at a time. For a read, the primary section rather than the abstract. Before a run of more than roughly half an hour, ask whether a smaller one answers the same question.
4. **Observe against the anchors.** Before any novel arm, place three anchors on your eval, because they answer different questions: a trivial baseline (majority class or chance, per task), the strongest known recipe run through its upstream code on your data, and the standard eval run on at least one published model. An internal reference (your own first run, a variant of your method) is none of these. A number means nothing without its baseline, its noise floor, and its evaluation conditions. Correctness before performance: a run that fails its checks scores nothing.
5. **Verdict: keep, revert, inconclusive, or failed.** Keep an improvement over the current best outside the noise floor under matched conditions; it becomes the new baseline. A kept win names its simplest other explanation (format or prompt adaptation, more steps or data, a lucky seed) and the control run that rules it out, or says it is not ruled out. Inside the noise floor is inconclusive, not a small win. **A result at trivial level is not a result:** stop comparing arms and diagnose the pipeline (overfit one tiny batch, check labels and the loss at init, look at the predictions, run the known recipe). Two runs there in a row and every further arm returns noise.
6. **Log it.** Hypothesis, prediction, config or commit, result, verdict, next ([format](references/research-log.md)). Predictions go in before results. Reverted and failed attempts stay. A campaign that lives in a repository keeps its journal, trial folders, and generated tables there ([shape](references/research-log.md#campaign-in-a-repository)).
7. **Decide.** Zoom in (converging evidence, or a genuine surprise), zoom out (nothing learned for a while, or the question was ill-posed), scale up (the small result survived its sanity checks), or write up (you could defend each claim to a skeptic).

Phases, timers, skepticism drills, and campaigns in detail: [research loop](references/research-loop.md).

## Using a lab

If a lab is present (a `lab.toml` above the working directory, or `lab` on PATH), let it hold the record instead of hand-kept files; the loop itself does not change. Without one, everything above works as before, and a single question does not need a lab.

- **Frame:** `lab new campaign <name> --metric <m> --goal min|max --trivial <value> --budget <usd> --question "..."`, then write the `plan` steps in `campaign.toml`. Data prep and the evaluator go in `locked/`, which is hashed on the first run. Anchors run as `lab run --anchor trivial|recipe|published`; one that cannot exist is waived with a reason (`waive = { published = "why" }`), never skipped; once you have measured the noise floor, write it as `noise_floor`.
- **Hypothesis and run:** `lab run --step <id> -H "<hypothesis>" -P "<prediction>" -D "if X do A, else B" -- <cmd>`, or `--off-plan "why"`; pipeline checks are `--kind smoke`. Fill the flags in before a peek.
- **Verdict:** `lab verdict <run> keep|revert|inconclusive|failed|reference -m "<why>" [--control <run>]`. Judge each run before the next. `keep` is refused at trivial level and while an anchor is missing; a run with neither `--step` nor `--off-plan` is refused; `reference` records a yardstick. Read `lab status` warnings; they are the plan and the gates.
- **Log:** run records replace the log table; `lab board --open` is the page to show, branching and eval changes are in the `lab` skill. Beliefs go in `findings.md` as bullets under "What we believe now", each citing its run ids; dead ends go under "What we tried that did not work".

## Guidance to load

- Training, fine-tuning, evaluation, or any run you launch: [experiment hygiene](references/experiment-hygiene.md). Read it before the first run, not after the first confusing result.
- Runs longer than a few minutes, GPUs, remote jobs: [long-running work](references/long-running-work.md), including the compute preflight (pinned env per recipe, one train and one eval step, one job first, eager before compile).
- Model, data, method, or benchmark selection and paper claims: [standard ML evidence](references/standard-ml.md).
- Circuits, probes, SAEs, patching, steering, any causal-mechanism claim: [mechanistic interpretability evidence](references/mech-interp.md).
- Anything that depends on a model, dataset, or codebase existing and working: [artifact verification](references/artifact-verification.md).
- Before reporting on anything larger than a quick answer: [failure modes](references/failure-modes.md), a short self-review that must change the report.

Running the jobs themselves (which service, LR and optimizer defaults, RL rewards, lm-eval and calibration) is the `ml-compute` skill; interpretability methods and tools are the `mech-interp` skill. Load only what the current pass needs.

## Evidence standard

Read the primary sections behind any load-bearing claim; abstracts and search snippets are for discovery only. Tie every result to its model or checkpoint, data, metric, baseline, and evaluation conditions. Vendor and paper numbers are reported results, not independent validation. Check recent releases before recommending; state the evidence cutoff. Look at the actual data and the actual outputs, never only the aggregate. Evaluate a repository, benchmark, or API through its own interface and bring the results back, rather than rebuilding it in a notebook and calling the number comparable.

## Scope and authorization

Research on its own does not authorize paid compute, training, or destructive changes to the user's environment. Within an authorized budget, keep going: make a reasonable assumption, verify it, and continue. If you believe you are blocked, show the evidence and keep looking for safe progress. Do not stop at a literature summary when experiments were authorized. Propose a discriminating experiment when uncertainty actually affects the decision; a paper explanation does not need an experiment plan attached.

## Control loop and workers

Run as one control-loop agent that owns the question, the log, and every verdict. Reading a result and deciding what it means stays in the controller, because that judgment needs the full history and is where research goes wrong. Workers execute.

- One worker owns the train and eval pipeline end to end, including "does it learn"; code is not passed between agents. Research workers read and report; they do not write runnable code. Fan out by question, not by arms that share one untested pipeline: those arms all fail together.

- Brief a worker with the intent, the starting state, the metric, and what evidence proves completion. Workers have latitude in how they execute: fix a crash, pick a sensible default, add a sanity check, read further when a source is thin.
- The one hard rule: every choice a worker made (seed, data slice, config change, skipped check, fix applied) goes in its [handoff record](references/research-log.md), so the controller sees it before judging the result. Decisions travel with context; an unreported choice is a future contradiction.
- Workers return the raw artifacts plus the record, not only a summary. Large outputs go to files the controller reads selectively.
- Delegation raises coverage, not honesty: a worker's "verified" is worker-reported evidence until the controller has read the artifact. A fresh-context verification worker is cheaper than trusting the implementation worker's judgment.
- Do single lookups and edits inline. Launch long runs non-blocking and keep working ([long-running work](references/long-running-work.md)).

## Mistakes you will make

- **Internal baseline taken for the baseline.** Your own first run is an ablation reference, not the known recipe or a published number.
- **Arms compared at chance.** Runs keep going after the pipeline stopped learning; each one returns noise.
- **The plan quietly changed.** The build differs from the plan (method, model, data, eval) and nobody said so.
- **Format gain reported as learning.** A fine-tune that only taught the output format; the control is a prompted or few-shot baseline.
- **Scope-changing fixes.** On an error you shrink the task (shorter sequences, LoRA for full tuning, another dataset); fix it minimally or ask.
- **A flag in `--help` trusted as a safety net.** Test the auto-stop, the timeout, the budget cap once before relying on it.

## Never

- Edit, re-tune, or regenerate the evaluation path, metric definition, or test split during a campaign. A run whose diff touches them is void, not a win.
- Select the reported result against the test set, or report the best of several runs as the result.
- Invent error bars or conditions you did not run, or a score for a run that failed.
- Drop failed, reverted, or interrupted runs from the log.
- Spend paid compute, train, or mutate the user's environment without authorization.

## Done

Before declaring completion, check the state against the postcondition you framed and every requirement of the original question, not against your memory of progress. Every number you lean on carries its baseline, repeats, and conditions; every claim traces to a run, a file, or a primary source you read; what remains untested is explicit. Budget exhaustion is not completion: report progress, the current best, blockers, and the concrete next experiment.

## Report

Lead with the answer, then the evidence, then the caveats, and size it to the task. Show the evidence (the command and what it returned, the per-seed numbers, the source section) rather than asserting success. Keep reported results, your inference, and your recommendation visibly distinct. Show randomly sampled examples, not the best ones. No file dumps.

For a single question: the answer in a sentence; confidence and its basis (verified by, or inferred from); the evidence with its conditions; what you could not verify; the one caveat most likely to make this wrong; the cheapest next step, if uncertainty matters.

For a campaign: the answer; confidence and the one thing that would change it; the current best with its baseline, delta, conditions, and per-run numbers; what changed, in order; tried and reverted, one line each so nobody repeats them; untested; next experiments with expected cost; links to commits, logs, and configs.
