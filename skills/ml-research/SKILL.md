---
name: ml-research
description: Drive ML research as an iterative loop (frame → hypothesis → cheapest experiment or read → observe → keep, revert, or inconclusive → log → decide) with primary-source evidence, experiment hygiene, and honest reporting. Use for any ML research question, method or model selection, training or eval campaign, ablation, reproducing a paper result, a training run that is not learning, a mechanistic-interpretability claim, or any "figure out whether X works" task, including when the user asks only a narrow question.
metadata:
  version: "2.2.0"
---

# ML Research

Own the research question, not the literal sentence the user typed. A narrow ask ("which model should I use", "does this paper's claim hold") is the entry point to a loop, not its end. Truth over an exciting answer: a surprising result earns more scrutiny, not less.

Match the effort to the question. A small question gets a paragraph with its evidence, not a narrated procedure. A campaign gets the whole loop and a log.

## The loop

A pass is one hypothesis tested by the cheapest thing that could change your mind: a read, a probe, or a run.

0. **Frame, once.** Restate the question, what is already known (a quick scan of the literature and the codebase, so you do not reinvent it), the budget, and what done looks like as something checkable. If the question as asked will not answer what the user actually wants, say so before spending real compute.
1. **Know the phase.** Explore (gain information), Understand (weigh named hypotheses against each other), or Distill (compress to 1–3 defensible claims). Say it only when it changes the plan. Most premature narrow answers come from acting as if in Understand while still in Explore, where the right move is many cheap probes and a long look at the data.
2. **State the hypothesis and what would falsify it.** Also the boring alternative explanation you must rule out.
3. **Do the cheapest decisive thing.** Smallest model, smallest data, shortest budget, one change at a time. For a read, the primary section rather than the abstract. Before a run of more than roughly half an hour, ask whether a smaller one answers the same question.
4. **Observe against a baseline.** A number means nothing without its baseline, its noise floor, and its evaluation conditions; a claim means nothing without the strongest competing source. Correctness before performance: a run that fails its checks scores nothing.
5. **Verdict: keep, revert, inconclusive, or failed.** Keep an improvement over the current best outside the noise floor under matched conditions; it becomes the new baseline. Inside the noise floor is inconclusive, not a small win. A neutral change that unlocks a branch you can name may be kept; log the reason.
6. **Log it.** Hypothesis, prediction, config or commit, result, verdict, next ([format](references/research-log.md)). Predictions go in before results. Reverted and failed attempts stay. A campaign that lives in a repository keeps its journal, trial folders, and generated tables there ([shape](references/research-log.md#campaign-in-a-repository)).
7. **Decide.** Zoom in (converging evidence, or a genuine surprise), zoom out (nothing learned for a while, or the question was ill-posed), scale up (the small result survived its sanity checks), or write up (you could defend each claim to a skeptic).

Phases, timers, skepticism drills, and campaigns in detail: [research loop](references/research-loop.md).

## Using a lab

If a lab is present (a `labs.toml` above the working directory, or `lab` on PATH), let it hold the record instead of hand-kept files; the loop itself does not change. Without one, everything above works as before, and a single question does not need a lab.

- **Frame:** `lab new campaign <name> --metric <m> --goal min|max --budget <usd> --question "..."`. Data prep and the evaluator go in `locked/`, which is hashed on the first run. Run the unchanged pipeline first and keep it as run zero; once you have measured the noise floor, write it as `noise_floor` in `campaign.toml` so the board shades the band.
- **Hypothesis and run:** `lab run -H "<hypothesis>" -P "<prediction>" -- <cmd>`. The flags are the prediction-before-result rule, so fill them in honestly rather than after a peek.
- **Verdict:** `lab verdict <run> keep|revert|inconclusive|failed -m "<why>"`. Judge each run before starting the next, since `keep` moves the baseline the next comparison uses.
- **Branch:** `lab new exp <name> --from <run>` starts from a run's exact code, so the board can diff against its parent; `--template <t>` starts a new kind of experiment (`lab templates`).
- **Log:** run records replace the log table. Beliefs go in `findings.md` as bullets under "What we believe now", each citing its run ids; dead ends go under "What we tried that did not work".
- **Eval changes:** a "locked/ changed" warning means runs on either side are no longer comparable. `lab lock --accept "why"` is for an intended, reported change, not a way to clear the warning.
- **Showing progress:** `lab board --open` is the staircase, lineage, and per-run diffs; figures made with `lab.fig` inside a run land in its record instead of loose files.

## Guidance to load

- Training, fine-tuning, evaluation, or any run you launch: [experiment hygiene](references/experiment-hygiene.md). Read it before the first run, not after the first confusing result.
- Runs longer than a few minutes, GPUs, remote jobs: [long-running work](references/long-running-work.md).
- Model, data, method, or benchmark selection and paper claims: [standard ML evidence](references/standard-ml.md).
- Circuits, probes, SAEs, patching, steering, any causal-mechanism claim: [mechanistic interpretability evidence](references/mech-interp.md).
- Anything that depends on a model, dataset, or codebase existing and working: [artifact verification](references/artifact-verification.md).
- Before reporting on anything larger than a quick answer: [failure modes](references/failure-modes.md), a short self-review that must change the report.

Running the jobs themselves (which service, LR and optimizer defaults, RL rewards, lm-eval and calibration) is the `ml-compute` skill; interpretability methods and tools are the `mech-interp` skill.

Load only what the current pass needs. A paper question in Explore needs the evidence reference, not the hygiene ladder.

## Evidence standard

Read the primary sections behind any load-bearing claim; abstracts and search snippets are for discovery only. Tie every result to its model or checkpoint, data, metric, baseline, and evaluation conditions. Vendor and paper numbers are reported results, not independent validation. Check recent releases before recommending; state the evidence cutoff. Look at the actual data and the actual outputs, never only the aggregate. Evaluate a repository, benchmark, or API through its own interface and bring the results back, rather than rebuilding it in a notebook and calling the number comparable.

## Scope and authorization

Research on its own does not authorize paid compute, training, or destructive changes to the user's environment. Within an authorized budget, keep going: make a reasonable assumption, verify it, and continue. If you believe you are blocked, show the evidence and keep looking for safe progress. Do not stop at a literature summary when experiments were authorized. Propose a discriminating experiment when uncertainty actually affects the decision; a paper explanation does not need an experiment plan attached.

## Control loop and workers

Run as one control-loop agent that owns the question, the log, and every verdict. Reading a result and deciding what it means stays in the controller, because that judgment needs the full history and is where research goes wrong. Workers execute.

- Brief a worker with the intent, the starting state, the metric, and what evidence proves completion. Workers have latitude in how they execute: fix a crash, pick a sensible default, add a sanity check, read further when a source is thin.
- The one hard rule: every choice a worker made (seed, data slice, config change, skipped check, fix applied) goes in its [handoff record](references/research-log.md), so the controller sees it before judging the result. Decisions travel with context; an unreported choice is a future contradiction.
- Workers return the raw artifacts plus the record, not only a summary. Large outputs go to files the controller reads selectively.
- Delegation raises coverage, not honesty: a worker's "verified" is worker-reported evidence until the controller has read the artifact. A fresh-context verification worker is cheaper than trusting the implementation worker's judgment.
- Do single lookups and edits inline. Launch long runs non-blocking and keep working ([long-running work](references/long-running-work.md)).

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
