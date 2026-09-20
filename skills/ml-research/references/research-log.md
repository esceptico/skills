# Research log and handoff

The log is the product of a research session as much as the answer. Decisions travel with context; an experiment that is not logged with its assumptions will be silently contradicted by a later one.

## Log table

Keep one file per campaign (for example `research-log.md` in the working directory, or the user's chosen tracker). Append a row per run or per probe. Write the prediction before the result.

| Run | Phase | Hypothesis | Predicted | Config / commit | Result | Verdict | Next |
| --- | --- | --- | --- | --- | --- | --- | --- |
| r07 | Understand | LR warmup is why r05 diverged | loss stable through step 200 | `a1b2c3d`, lr 3e-4, warmup 100 | stable, val 2.41 vs best 2.44 | keep, new best | try warmup 50 |

Verdicts are `keep`, `revert`, `inconclusive`, or `failed` with a reason. Rejected and failed runs stay in the table. A result without its baseline and conditions is not a result.

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
