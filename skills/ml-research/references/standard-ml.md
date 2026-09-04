# Standard ML Evidence Pattern

Use this reference for training, fine-tuning, inference, architecture, dataset, benchmark, and ML systems questions.

## Core evidence unit

`dataset + model/checkpoint + method + configuration → measured result`

A result without its conditions is not actionable.

## Current-artifact scan

Before selecting a contemporary model, dataset, or implementation:

1. Check recent releases in the relevant official repositories. For Hugging Face selection, use both `createdAt` and `lastModified` ordering when available; otherwise inspect release history or model cards for those dates. Modification alone does not establish a new model release.
2. Filter by the user's size, task, modality, license, and deployment constraints.
3. Compare plausible eligible alternatives, including newer releases missing from older paper citations. Choose breadth based on the decision; do not pad the comparison to a fixed count.
4. Record why the selected artifact wins and why each serious alternative was rejected.
5. Treat vendor benchmark claims as evidence to reproduce, not independent validation.

## Evidence to inspect

Use the fields relevant to the claim or selection. Missing training details need not block a dataset comparison; missing evaluation conditions may block a performance ranking.

### Publication

- Title, identifier, date, venue, and publication status
- Exact section, table, figure, or appendix supporting the claim

### Data

- Dataset IDs and sources
- Config, split sizes, evaluation split, and schema
- Filtering, deduplication, preprocessing, augmentation, and mixtures
- Prompt/chat format or label definition
- License, access restrictions, and contamination concerns

### Model

- Architecture, size, exact checkpoint, tokenizer or processor
- Base initialization and context length or resolution
- Precision and parameter-efficient versus full training

### Method and configuration

- Objective and loss
- Optimizer, learning rate, schedule, and warmup
- Steps or epochs
- Per-device and effective batch size
- Gradient accumulation and clipping
- Sequence length or input resolution
- Important method-specific settings
- Hardware and compute when reported

### Evaluation

- Exact metric and score
- Evaluation protocol, prompt/template, and harness
- Number of samples, seeds, and uncertainty when reported
- Baseline and ablation comparisons
- Whether compared systems use equivalent data, scale, retrieval, tools, and compute

### Artifacts

- Exact Hugging Face model and dataset IDs
- Code repository and implementation/config file paths
- Checkpoints, evaluation scripts, and current documentation
- Verification status: `verified`, `partial`, `unverified`, or `unavailable`

## Comparability gate

Do not rank headline numbers directly when metrics, splits, prompting, harnesses, data, model scale, compute, or run-selection procedures differ. State the confound and restrict the conclusion.

## Recommendation gate

Before recommending a method, answer:

1. Is the advantage supported by an appropriate comparison?
2. Are required data, code, licenses, and checkpoints available?
3. Does the implementation use current APIs?
4. Does it fit the user's compute, time, and deployment constraints?
5. What is the smallest real-path smoke test?

A good first experiment reproduces one defensible baseline, changes one justified factor, preserves the evaluation protocol, and records both quality and resource metrics.
