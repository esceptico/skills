# Long-running work

Applies to training runs, large evals, sweeps, remote GPUs, and any job that outlives a single turn. Shape borrowed from Prime Intellect's agent conventions.

## Smoke test before scale

Run the full path once at the smallest scale that exercises it: a handful of samples, one step, one seed. Confirm the metric is computed, outputs look sane, and the resolved config matches the plan: code revision, dependency versions, and the settings your task actually varies (generation flags and the rendered prompt for LLM evals, preprocessing and augmentation for vision, the reward for RL). A flat metric or reward at baseline is a broken pipeline, not a hard task. Only then scale.

## Compute preflight

Before a paid or long job, after [ml-intern](https://github.com/huggingface/ml-intern)'s preflight (`agent/prompts/system_prompt_v3.yaml`). If an item cannot be filled in, do that first.

- **Pinned environment per recipe.** Each upstream recipe runs in its own environment at the versions it pins (its lockfile or requirements, its commit), not in yours. Print the installed versions before the model loads.
- **One train step and one eval step** on the same entrypoint, data columns, model-loading path, precision and attention settings as the real job, on the same kind of machine. Submit the exact script you tested, not a rewrite.
- **Eager before compile.** Get a correct eager run first; turn on `torch.compile`, CUDA graphs or fused kernels only after, and check the metric did not move.
- **One job first.** For a sweep or a batch, start one job, see it train and log, then start the rest: they would all fail on the same bug.
- **Safety nets are tested, not read.** A timeout, an auto-stop or a budget flag that appears in `--help` is not proof it is enforced; check it once on something cheap.

## Non-blocking control loop

Start the job, record its handle and output location, then do other useful work instead of blocking on a sleep. If your harness stops when you stop, schedule the check-back (a background task with a notification, a heartbeat) or tell the user when to resume. Check back on a schedule proportional to the job's expected length, read the tail of the log or the metrics file, and decide: continue, stop, or launch the next variant. Stop broken or uninformative runs early; an interrupted run is not a negative result and is logged as interrupted.

## Compute ladder

Local kernel or REPL for probes, a disposable sandbox or single GPU for pilots, multi-GPU or cluster only for the run that the pilot justified. Each step up needs a reason recorded in the log. Estimate cost and time before launching; compare the expected information from a bigger run against the next cheap experiment.

## Retain everything that a re-run needs

Pin code, model, and data revisions, save the resolved config next to the results, and keep failed-run artifacts. Large outputs belong in files you read selectively, not in the conversation.
