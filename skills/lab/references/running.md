# Running, logging, remote machines, reports

Generated from `~/src/labs` at cc04a44 2026-09-23 by `scripts/skill_reference.py`. Regenerate after changing the lab; if this disagrees with `lab <cmd> --help`, the CLI wins.

## Logging from inside a run

Logging from code running under `lab run`.

    from lab import log, summary, cost, artifact, fig

    log(step=100, loss=0.41, jac_rank=37)   # a point on a curve
    summary(val_loss=0.38)                  # the numbers this run is judged by
    cost(1.20, "tinker sft")                # money spent outside this machine
    artifact("spectrum.png", "Jacobian spectrum, layer 12")

Outside `lab run` every call does nothing, so the same script runs standalone.

This module, `lab.fig`, `lab.events`, `lab.remote` and the runnable entrypoints (`lab.modal_app`,
`lab.ssh_app`, `lab.bench_run`, `lab.hf_fetch`) run inside experiment environments and use the
standard library only. The CLI's internals live in `lab.core`, `lab.views` and `lab.ops`.

Environment set by `lab run`: `LAB_RUN_DIR`, `LAB_RUN_ID`, `LAB_CAMPAIGN_DIR`, `LAB_LOCKED_DIR`, `LAB_HOME`; `PYTHONPATH` gets the `lab` package and `lib/`, so any interpreter or venv can `from lab import ...` and import `lib/` modules.

## Templates

- `interp`: A Jacobian-subspace experiment on any Hugging Face causal LM, with controls built in.
- `modal-custom`: Plain PyTorch you own completely: custom architectures, losses on activations, anything Tinker
- `prime-rl`: RL (or SFT distillation) on Prime Intellect Hosted Training, recorded as a lab run.
- `tinker-sft`: LoRA supervised fine-tuning on Tinker, with room for your own loss.

Start one with `lab new exp <name> --template <template>`; each folder has a README with the exact command.

## Modal: lab.modal_app

Run any experiment script on a Modal GPU and bring its lab outputs home.

    lab run -H "..." -- modal run -m lab.modal_app --script train.py --args "--lr 3e-4" --gpu A10

The experiment folder, the campaign's locked/ folder and the lab's lib/ are shipped into the
container; `requirements.txt` in the experiment folder is installed into the image (cached).
Inside, the script logs with `lab.log` / `lab.fig` as usual; when it ends, metrics, figures and
artifacts are copied into the local run. Checkpoints belong in $LAB_DATA_DIR (the `lab-data`
volume), not in artifacts. Cost is not logged: Modal bills your account, and lab records only
amounts a service reports.

Needs `pip install modal` and `modal token new` once.

Options of the local entrypoint: `--script` (default train.py), `--args` (quoted), `--gpu` (T4, L4, A10, L40S, A100-40GB, A100-80GB, H100, H200, B200; `:N` for several), `--timeout-hours` (default 6).

## Any SSH machine: lab.ssh_app

Run an experiment script on any machine you can SSH into (a RunPod or Prime pod, Lambda, your own box).

    lab run -H "..." -- python -m lab.ssh_app --host root@203.0.113.7 --port 22042 \
        --script train.py --args "--lr 3e-4"

Copies the experiment folder, the campaign's locked/, the lab's lib/ and the lab package to
<root>/<run id> with rsync, installs requirements.txt if present, runs the script there with
output streamed here, and copies metrics, figures and artifacts back into the run. HF_TOKEN is
passed in a 0600 env file, not argv. Cost is not logged: lab records only amounts a service reports.
Checkpoints: write them under --root on the machine (a network volume on RunPod), not artifacts.
`--host local` runs the same steps without SSH (for testing the path).

```
usage: ssh_app.py [-h] --host HOST [--port PORT] [--key KEY] [--root ROOT]
                  [--script SCRIPT] [--args ARGS] [--python PYTHON]
                  [--no-setup]

options:
  -h, --help       show this help message and exit
  --host HOST      user@host, or 'local'
  --port PORT
  --key KEY        ssh identity file
  --root ROOT      working directory on the machine (relative to home, or
                   absolute)
  --script SCRIPT
  --args ARGS
  --python PYTHON
  --no-setup       skip pip install -r requirements.txt
```

## Remote outputs: lab.remote

Moving a run's outputs back from a remote machine.

Remote code logs into its own scratch run directory (LAB_RUN_DIR there); when it finishes,
`pack` collects what `lab` records and `unpack` merges it into the real run directory here.

## Benchmarks: lab bench

Run lm-evaluation-harness inside a lab run; record every metric, plus ECE and Brier for multiple-choice tasks.

Started by `lab bench`. For multiple-choice tasks, a softmax over the choices' log-likelihoods gives a
probability per choice. The samples format was checked against lm-eval d6de8164: `filtered_resps` holds
[loglikelihood, is_greedy] per choice (written as strings), and `target` is the gold index or answer text.

## Reports: lab report

`lab report <campaign>`: a self-contained interactive page from report.md (or findings.md).

Markdown (CommonMark + tables), plus:
  - run ids (r008) become links that show the run's evidence on hover;
  - a line `{{figure <name> runs=r003,r008,r004 labels="k = 4,k = 8,k = 16" label="k"}}` embeds that
    figure from each listed run; with several runs it becomes a switcher over those recorded runs
    only (compare toggles, steppers), never interpolated;
  - the page ends with the runs cited, what did not work, and how to reproduce each cited run.
Figure names are the file stems in runs/<id>/figures/ (a slug of the figure's title).
