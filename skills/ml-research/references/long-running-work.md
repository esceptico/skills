# Long-running work

Applies to training runs, large evals, sweeps, remote GPUs, and any job that outlives a single turn. Shape borrowed from Prime Intellect's agent conventions.

## Smoke test before scale

Run the full path once at the smallest scale that exercises it: a handful of samples, one step, one seed. Confirm the metric is computed, outputs look sane, and the resolved config matches the plan: code revision, dependency versions, and the settings your task actually varies (generation flags and the rendered prompt for LLM evals, preprocessing and augmentation for vision, the reward for RL). A flat metric or reward at baseline is a broken pipeline, not a hard task. Only then scale.

## Non-blocking control loop

Start the job, record its handle and output location, then do other useful work instead of blocking on a sleep. If your harness stops when you stop, schedule the check-back (a background task with a notification, a heartbeat) or tell the user when to resume. Check back on a schedule proportional to the job's expected length, read the tail of the log or the metrics file, and decide: continue, stop, or launch the next variant. Stop broken or uninformative runs early; an interrupted run is not a negative result and is logged as interrupted.

## Compute ladder

Local kernel or REPL for probes, a disposable sandbox or single GPU for pilots, multi-GPU or cluster only for the run that the pilot justified. Each step up needs a reason recorded in the log. Estimate cost and time before launching; compare the expected information from a bigger run against the next cheap experiment.

## Retain everything that a re-run needs

Pin code, model, and data revisions, save the resolved config next to the results, and keep failed-run artifacts. Large outputs belong in files you read selectively, not in the conversation.
