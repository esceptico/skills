---
name: ml-research
description: Drive ML research as an iterative loop (hypothesis → cheapest experiment → observe → keep or revert → log → decide) with primary-source evidence, experiment hygiene, and honest reporting. Use for any ML research question, method or model selection, training or eval campaign, ablation, mechanistic-interpretability claim, or "figure out whether X works" task, including when the user asks only a narrow question.
metadata:
  version: "2.0.0"
---

# ML Research

Own the research question, not the literal sentence the user typed. A narrow ask ("which model should I use", "does this paper's claim hold") is the entry point to a loop, not its end. Truth over an exciting answer: a surprising result earns more scrutiny, not less.

## The loop

Every turn of work is one pass through this loop. Keep the pass small and the log honest.

1. **Declare the phase.** Explore (gain information), Understand (discriminate between named hypotheses), or Distill (compress to 1–3 defensible claims). Say which one you are in and why. Most premature narrow answers come from acting as if in Understand while still in Explore.
2. **State the hypothesis and its falsifier.** One sentence each. Also write the boring alternative explanation you must rule out.
3. **Run the cheapest experiment that could change the decision.** Smallest model, smallest data, shortest budget, one change at a time. Before any run longer than ~30 minutes, ask whether a smaller one would answer the same question.
4. **Observe against a baseline and a noise floor.** No number means anything without its baseline, seed variation, and evaluation conditions. Correctness gates come before performance: a wrong result scores zero, not "fast".
5. **Keep or revert.** Improvement against the current best under matched conditions is kept and becomes the new baseline. Anything else is reverted. Record both.
6. **Log it.** Append to the research log ([format](references/research-log.md)): hypothesis, config or commit, result, verdict, next. Predictions go in before results.
7. **Decide.** Zoom in (converging evidence or a genuine surprise), zoom out (nothing new learned in a while, or the question was ill-posed), scale up (the small result survived its sanity checks), or write up (you would defend each claim to a skeptic).

Detailed guidance on phases, timers, skepticism drills, and the statistical bar: [research loop](references/research-loop.md).

## Guidance to load

- Training, fine-tuning, evaluation, or any run you launch: [experiment hygiene](references/experiment-hygiene.md). Read it before the first run, not after the first confusing result.
- Runs longer than a few minutes, GPUs, remote jobs: [long-running work](references/long-running-work.md).
- Model, data, method, or benchmark selection and paper claims: [standard ML evidence](references/standard-ml.md).
- Circuits, probes, SAEs, patching, steering, any causal-mechanism claim: [mechanistic interpretability evidence](references/mech-interp.md).
- Anything that depends on a model, dataset, or codebase existing and working: [artifact verification](references/artifact-verification.md).
- Before reporting: [failure modes](references/failure-modes.md), a self-review that must change the report.

Load only what the current pass needs. A narrow paper question in Explore needs the evidence reference, not the hygiene ladder.

## Evidence standard

Read the primary sections behind any load-bearing claim; abstracts and search snippets are for discovery only. Tie every result to its model or checkpoint, data, metric, baseline, and evaluation conditions. Vendor and paper numbers are reported results, not independent validation. Check recent releases before recommending; state the evidence cutoff. Look at the actual data and the actual outputs, never only the aggregate.

## Scope and authorization

Research on its own does not authorize paid compute, training, or destructive changes to the user's environment. Within an authorized budget, keep going: make a reasonable assumption, verify it, and continue. Do not stop at a literature summary when experiments were authorized, and do not launch experiments to earn a stronger label when a literature answer was requested.

## Control loop and workers

Run as one control-loop agent that owns the question, the log, and every keep-or-revert verdict. Reading a result and deciding what it means stays in the controller, because that judgment needs the full history and is where research goes wrong. Workers execute.

- Brief a worker with the intent, the starting state, the metric, and what evidence proves completion. Workers have latitude in how they execute: fix a crash, pick a sensible default, add a sanity check, read further when a source is thin.
- The one hard rule: every choice a worker made (seed, data slice, config change, skipped check, fix applied) goes in its [handoff record](references/research-log.md), so the controller sees it before judging the result. Decisions travel with context; an unreported choice is a future contradiction.
- Workers return the raw artifacts plus the record, not only a summary. Large outputs go to files the controller reads selectively.
- Worker results are worker-reported evidence until the controller has read the artifact. A fresh-context verification worker is cheaper than trusting the implementation worker's judgment.
- Do single lookups and edits inline. Launch long runs non-blocking and keep working ([long-running work](references/long-running-work.md)).

## Done

Before declaring completion, audit the state against every requirement of the original question, not against your memory of progress. Completion means:

- the decision or claim is answered with evidence traceable to a run, a file, or a primary source you read;
- baselines, seeds or repeats, and evaluation conditions are stated for every number you lean on;
- negative and reverted attempts are in the log, not erased;
- what remains untested is explicit.

Budget exhaustion is not completion. When the budget ends, report progress, the current best, blockers, and the concrete next experiment.

## Report

Lead with the answer or the current best, then the decisive evidence, then caveats. Report randomly sampled examples, not the best ones. Keep reported results, your inference, and your recommendation visibly distinct. Use the depth the question needs; a paper explanation does not need an experiment plan, and a campaign does not fit in one paragraph.
