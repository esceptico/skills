# Long-running work

Applies to training runs, large evals, sweeps, remote GPUs, and any job that outlives a single turn. Shape borrowed from Prime Intellect's agent conventions.

## Smoke test before scale

Run the full path once at the smallest scale that exercises it: a handful of samples, one step, one seed. Confirm the metric is computed, outputs look sane, and the resolved config matches the plan (deployed source hash, dependency versions, generation flags, full prompt construction). For RL or reward-based setups, confirm reward diversity exists at baseline; a flat reward is a broken pipeline, not a hard task. Only then scale.

## Non-blocking control loop

Start the job, record its handle and output location, then end the turn or move to other work. Do not hold the turn open with sleeps or long blocking waits. Check back on a schedule proportional to the job's expected length, read the tail of the log or the metrics file, and decide: continue, stop, or launch the next variant. Stop broken or uninformative runs early; an interrupted run is not a negative result and must be logged as interrupted.

## Compute ladder

Local kernel or REPL for probes, a disposable sandbox or single GPU for pilots, multi-GPU or cluster only for the run that the pilot justified. Each step up needs a reason recorded in the log. Estimate cost and time before launching; compare the expected information from a bigger run against the next cheap experiment.

## Evaluate external systems through their own interface

A repository, benchmark, dataset, or API has its own environment and normal entry points. Use them, then bring the results back for analysis. Do not rebuild a benchmark harness inside a notebook and call the number comparable.

## Retain everything that a re-run needs

Pin code, model, and data revisions, save the resolved config next to the results, and keep failed-run artifacts. Large outputs belong in files you read selectively, not in the conversation.
