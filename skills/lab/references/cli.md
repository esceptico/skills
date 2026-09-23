# lab CLI reference

Generated from `~/src/labs` at cc04a44 2026-09-23 by `scripts/skill_reference.py`. Regenerate after changing the lab; if this disagrees with `lab <cmd> --help`, the CLI wins.


```
usage: lab [-h] [-c CAMPAIGN] command ...

lab: run anything, record every run, compare honestly.

lab new campaign <name> --metric val_loss --goal min --budget 50
lab new exp <name> [--from <exp|run> | --template <name>]   (lab templates)
lab run -H "hypothesis" -P "prediction" -- python train.py --lr 3e-4
lab ls | lab show <run> | lab verdict <run> keep|revert|inconclusive|failed -m "why"
lab lock --accept "why the eval changed" | lab budget | lab board --open
lab bench <model> --tasks a,b | lab fetch model|dataset <repo>[@rev] | lab doctor | lab smoke [--live]
lab report <campaign> --open

positional arguments:
  command
    new                 create a campaign or an experiment
    templates           list experiment templates
    run                 run a command and record it
    ls                  list runs
    show                print a run record
    verdict             judge a run; keep makes it the baseline
    lock                accept a change to locked/ and start a new comparison
                        epoch
    budget              spend against the cap
    board               write the board: one HTML page over every campaign
    bench               run lm-evaluation-harness as a recorded run (accuracy
                        + calibration)
    fetch               download a HF model or dataset at a pinned revision
    doctor              check tools, keys and logins for every service
    smoke               run templates on tiny configs to catch breakage
    report              write an interactive report page for a campaign

options:
  -h, --help            show this help message and exit
  -c, --campaign CAMPAIGN
                        campaign name (default: the one around the current
                        directory)
```

## lab new campaign

```
usage: lab new campaign [-h] [--question QUESTION] [--metric METRIC]
                        [--goal {min,max}] [--budget BUDGET]
                        name

positional arguments:
  name

options:
  -h, --help           show this help message and exit
  --question QUESTION
  --metric METRIC
  --goal {min,max}
  --budget BUDGET
```

## lab new exp

```
usage: lab new exp [-h] [--from SOURCE | -t TEMPLATE] name

positional arguments:
  name

options:
  -h, --help            show this help message and exit
  --from SOURCE         an experiment name or a run id to branch from
  -t, --template TEMPLATE
                        start from <lab>/templates/<name> (see `lab
                        templates`)
```

## lab templates

```
usage: lab templates [-h]

options:
  -h, --help  show this help message and exit
```

## lab run

```
usage: lab run [-h] [-H HYPOTHESIS] [-P PREDICTION] [--parent PARENT] [-e EXP]
               [-t TAG]
               ...

positional arguments:
  command

options:
  -h, --help            show this help message and exit
  -H, --hypothesis HYPOTHESIS
  -P, --prediction PREDICTION
                        what you expect, written before the result
  --parent PARENT       run this one builds on (default: previous run of this
                        experiment)
  -e, --exp EXP         experiment name (default: the one around the current
                        directory)
  -t, --tag TAG
```

## lab ls

```
usage: lab ls [-h]

options:
  -h, --help  show this help message and exit
```

## lab show

```
usage: lab show [-h] run

positional arguments:
  run

options:
  -h, --help  show this help message and exit
```

## lab verdict

```
usage: lab verdict [-h] [-m NOTE] run {keep,revert,inconclusive,failed}

positional arguments:
  run
  {keep,revert,inconclusive,failed}

options:
  -h, --help            show this help message and exit
  -m, --note NOTE
```

## lab lock

```
usage: lab lock [-h] --accept WHY

options:
  -h, --help    show this help message and exit
  --accept WHY
```

## lab budget

```
usage: lab budget [-h]

options:
  -h, --help  show this help message and exit
```

## lab board

```
usage: lab board [-h] [--out OUT] [--open]

options:
  -h, --help  show this help message and exit
  --out OUT   output directory (default: <lab>/board)
  --open      open it in the browser
```

## lab bench

```
usage: lab bench [-h] --tasks TASKS [--model-type MODEL_TYPE]
                 [--model-args MODEL_ARGS] [--limit LIMIT]
                 [--num-fewshot NUM_FEWSHOT] [--extra EXTRA] [-H HYPOTHESIS]
                 [-P PREDICTION] [--parent PARENT]
                 model

positional arguments:
  model                 HF id or local path (or served model name with
                        --model-type local-completions)

options:
  -h, --help            show this help message and exit
  --tasks TASKS         comma-separated lm-eval tasks, e.g.
                        gpqa_diamond_zeroshot,mmlu_pro
  --model-type MODEL_TYPE
                        lm-eval --model: hf, vllm, local-completions, ...
  --model-args MODEL_ARGS
                        extra lm-eval model_args, e.g.
                        dtype=bfloat16,peft=path
  --limit LIMIT         examples per task (or fraction) for a quick look
  --num-fewshot NUM_FEWSHOT
  --extra EXTRA         more lm_eval flags, quoted
  -H, --hypothesis HYPOTHESIS
  -P, --prediction PREDICTION
  --parent PARENT
```

## lab fetch

```
usage: lab fetch [-h] [--include INCLUDE] {model,dataset} repo

positional arguments:
  {model,dataset}
  repo               org/name[@revision]

options:
  -h, --help         show this help message and exit
  --include INCLUDE  only files matching this glob (repeatable)
```

## lab doctor

```
usage: lab doctor [-h]

options:
  -h, --help  show this help message and exit
```

## lab smoke

```
usage: lab smoke [-h] [--live] [--only ONLY [ONLY ...]]

options:
  -h, --help            show this help message and exit
  --live                also check Tinker imports, Prime and Modal auth
  --only ONLY [ONLY ...]
                        template or service names
```

## lab report

```
usage: lab report [-h] [--out OUT] [--open] name

positional arguments:
  name        campaign name

options:
  -h, --help  show this help message and exit
  --out OUT   output directory (default: <lab>/reports)
  --open
```
