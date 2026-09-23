---
name: lab
description: Operate the `lab` research CLI (~/src/labs) - campaigns, `lab run` records, verdicts and baselines, locked evals, budgets, templates, lab.fig figures, the board, lm-eval benches, pinned downloads, Modal and SSH runners, smoke checks, and interactive reports. Use whenever a `labs.toml` is above the working directory or `lab` is on PATH, when the user mentions the lab, a campaign, a run id like r012, the board or a report, or asks to set up a new lab.
metadata:
  version: "1.0.0"
---

# lab

`lab` wraps any command, records every run, and keeps comparisons honest. This skill is how to drive it; how to do the research is `ml-research`, where to run it is `ml-compute`, interpretability methods are `mech-interp`.

## Get oriented first

- `lab doctor` says which services are ready (Tinker key, Prime login, Modal, RunPod, Hugging Face, disk). Run it before promising a route.
- `lab ls` (inside a campaign, or `lab -c <name> ls`) shows runs, the baseline (`*`), verdicts and cost; `lab show r012` prints one record; `lab board --open` shows everything.
- Read the campaign's `campaign.toml` (question, metric, goal, budget, noise floor) and `findings.md` before proposing the next run.

## The cycle

```bash
lab new campaign <name> --metric val_loss --goal min --budget 25 --question "..."
lab new exp <name> --template interp        # or --from r012 to branch from a run's exact code
lab run -H "hypothesis" -P "prediction" -- python train.py --lr 3e-4
lab verdict r013 keep|revert|inconclusive|failed -m "why"
lab report <campaign> --open                # when there is something to show
```

Inside the code: `from lab import log, summary, cost, artifact, fig`. Log curves with `log(step=..., **values)`, the numbers the run is judged by with `summary(...)`, off-machine spend with `cost(usd, note)`, and figures with `fig.<type>(...)`. Outside `lab run` they do nothing, so scripts still run standalone.

## Rules of thumb

- Put data prep and the evaluator in the campaign's `locked/` before the first run; it is hashed then. If it changes later, runs are marked not comparable until `lab lock --accept "why"`, which is for a deliberate, reported change only.
- Judge each run before starting the next: `keep` moves the baseline that comparisons and new experiments start from. A run's parent defaults to the previous run of the same experiment; pass `--parent` when it builds on something else.
- Branch with `lab new exp <name> --from <run>` instead of copying files, so the board can diff code against the parent.
- A helper used by a second experiment belongs in the lab's `lib/` (on every run's path, snapshotted and hashed per run).
- Set `noise_floor` in `campaign.toml` once seeds have measured it, so deltas inside it read as inconclusive.
- Paid services: start with the smallest config. The budget counts only real amounts (Prime's reported spend, `cost()` calls); Modal, SSH machines and Tinker bill your accounts directly.

## When something is off

- **Budget refusal:** the campaign's `cost_usd` total reached `budget_usd`. Raise it in `campaign.toml` only if the user agrees.
- **"locked/ changed" warning:** someone edited the eval. Find out whether it was intended before accepting.
- **Run stuck at `running`:** the `lab` process was killed hard. Its record stays as it was; judge it `failed -m "killed"` and rerun.
- **Command not found / service errors:** `lab doctor`; for templates that stopped working, `lab smoke` (add `--live` for services).
- **Report figure errors:** figure names are file stems in `runs/<id>/figures/`; the error lists the ones that exist.

## New lab

A lab is a folder with `labs.toml` (plus `campaigns/`, `lib/`, `templates/`); `~/src/labs` is the main one. Install the CLI once with `uv tool install -e ~/src/labs`; set `LAB_HOME` when working outside the folder.

## Reference

- [cli.md](references/cli.md): every command and flag (generated from `--help`).
- [figures.md](references/figures.md): all ten `lab.fig` chart types with signatures and examples.
- [running.md](references/running.md): logging helpers and environment, templates, Modal and SSH runners, bench, reports.

These are generated from the code by `~/src/labs/scripts/skill_reference.py`; when they disagree with `lab <cmd> --help`, trust the CLI and regenerate.
