# Research log and handoff

The log is the product of a research session as much as the answer. Decisions travel with context; an experiment that is not logged with its assumptions will be silently contradicted by a later one.

## Log table

For a campaign, or work that crosses sessions or agents, keep one log file where the user wants it (a `research-log.md` next to the code, or their tracker). For a short question the log is your own context; do not leave files in the user's repo. Append a row per run or probe, and write the prediction before the result.

| Run | Phase | Hypothesis | Predicted | Config / commit | Result | Verdict | Next |
| --- | --- | --- | --- | --- | --- | --- | --- |
| r07 | Understand | LR warmup is why r05 diverged | loss stable through step 200 | `a1b2c3d`, lr 3e-4, warmup 100 | stable, val 2.41 vs best 2.44 | keep, new best | try warmup 50 |

Verdicts are `keep`, `revert`, `inconclusive`, or `failed` with a reason. Reverted and failed runs stay in the table. Record per-run numbers, not only the mean. A result without its baseline and conditions is not a result.

Keep a short highlights section above the table: the current best, the two or three most surprising findings, and open anomalies.

## Handoff record

When a session ends, context is compacted, a worker returns to the control loop, or work moves to another agent, write a record with these headings. Keep it declarative; it describes the state, not future plans dressed as facts.

- **Question and constraints:** what is being decided, the budget, what is off limits.
- **Decisions:** what was chosen and what was rejected, with the reason. Include implicit choices (seed, data slice, eval protocol) that later work must not contradict.
- **Current best:** the run, its config, its number, its baseline.
- **Verification and failures:** exact commands, working directory, pass and fail counts, the decisive diagnostics, checks that were skipped.
- **Known-good versus known-broken:** environment caveats, setup steps that worked, what still fails.
- **Untested:** what the evidence does not cover.
- **Next useful starting point:** the one experiment or read that should happen first.

Distinguish evidence you observed from evidence a subagent or a paper reported. Note when later changes may have invalidated an earlier verification.

## Campaign in a repository

When a campaign is authorized and lives in a repository, keep the record in the repo, in this shape. Skip all of it for a single question.

- **One journal file** (for example `PLAN.md`) that opens with the current decision, then a corrections section that retracts earlier claims the evidence no longer supports, then dated notes that say what did not work as plainly as what did. Every claim links to the result file it rests on.
- **One folder per trial** (`runs/<study>/NN-<label>/`) holding the resolved config, the result, and the raw log. A study keeps one ledger with a line per trial: id, status, objective, verdict, cost. The log table above is that ledger in prose form.
- **Tables and figures are generated from result files** by a script checked into the repo. No number in the journal or the README is typed by hand, so a regenerated table cannot disagree with the runs.
- **Evaluation data is frozen** with a manifest of hashes and versions. New data is a new version, never an edit. The test split is read once, at the end, and the journal names the run it was read for.
- **Cost per run** (GPU time or dollars) sits next to the metric, so a small gain that cost most of the budget reads as what it is.
- **Shared code is promoted, not copied.** While a change is being tried, keep it in the trial's own code, so the diff against its parent shows exactly what changed. Once a helper (a loader, a hook, a plotting function) is used by a second experiment and has stopped changing, move it to one shared module (`lib/` in a lab) rather than copying it again. The evaluator stays in the frozen eval path, not the shared module. Shared code is part of what ran: a lab snapshots `lib/` into each run and records its hash, so the diff against the parent shows a `lib/` edit; elsewhere, record the shared module's commit with the run. After editing something a kept run used, re-run the baseline before comparing across the edit.

