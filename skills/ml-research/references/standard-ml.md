# Standard ML Evidence Pattern

Use this reference for training, fine-tuning, inference, architecture, dataset, benchmark, and ML systems questions.

## Core evidence unit

`dataset + model/checkpoint + method + configuration → measured result`

A result without its conditions is not actionable.

## Current-artifact scan

For contemporary selection, check recent official releases that meet the user's constraints, including plausible alternatives missing from older citations. Release histories, model cards, and repository date filters can help; modification alone does not establish a new release.

Choose comparison breadth according to the decision and explain the consequential tradeoffs. Treat vendor benchmark claims as reported results, not independent validation.

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
- Verification depth and revision: use [artifact verification](artifact-verification.md).

## Comparability gate

Do not rank headline numbers directly when metrics, splits, prompting, harnesses, data, model scale, compute, or run-selection procedures differ. State the confound and restrict the conclusion.

## Selection bias and uncertainty

For performance claims, inspect variation across relevant seeds and data splits, effect sizes, and reported uncertainty. Missing uncertainty limits the conclusion; do not invent error bars or assume a small improvement is robust.

Compare tuning and selection budgets as well as final training cost: trials, prompts, checkpoints, and metrics searched can change the best reported score. Check whether the final evaluation data were held out from model, prompt, and hyperparameter selection. Repeatedly choosing against the test set makes it part of selection.

When assessing a claimed win, look for matched evaluation conditions and an untouched evaluation or independent replication. Account for multiple comparisons when many alternatives were screened. Where those checks are unavailable, describe the result as a reported gain with unresolved selection bias rather than an established advantage.

## Recommendations

Base the recommendation on comparable evidence, usable artifacts, and the user's constraints. When an experiment is useful, choose one that resolves the main uncertainty with an appropriate baseline and evaluation protocol; record quality and resource costs relevant to the decision.
