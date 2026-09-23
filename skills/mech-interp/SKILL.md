---
name: mech-interp
description: Methods and tooling for mechanistic interpretability on transformer LMs - Jacobians between residual layers and their singular subspaces, subspace ablation, activation patching, steering, interchange interventions, SAEs, and the libraries for each (plain torch hooks, nnsight/NDIF, TransformerLens, pyvene, SAELens). Use when designing or running an interpretability experiment, choosing an intervention or its controls, picking a tool, or scaling an interp run from a small model to a large one.
metadata:
  version: "1.0.0"
---

# Mechanistic Interpretability

How to measure what a model computes internally, with controls that tell a mechanism from generic damage. What counts as evidence for a causal claim (necessity, sufficiency, specificity, generalization) is the `ml-research` skill's evidence standard, `references/mech-interp.md`; this skill is the method and the tools.

## Choose the method by the claim

- **"This low-dimensional subspace carries the computation between layers L and M":** Jacobians between residual layers, their SVD, and ablating the top directions. [Jacobian subspaces](references/jacobian-subspaces.md) covers what J does and does not measure, cost at large d, reading the spectrum, projection vs mean vs resample ablation, and the controls this method needs (random bases, removed norm and PCA baselines, random-init weights, a linearisation check).
- **"This site matters for this behaviour":** activation patching, with the direction (noising or denoising) chosen for the question. **"This direction controls it":** steering, with a scale sweep and an off-distribution check. **"This variable is represented here":** interchange interventions or DAS. [Interventions](references/interventions.md).
- **"These features explain it":** SAEs, with their health (L0, loss recovered, dead features) checked first, since a poor SAE explains its own errors. [Tooling](references/tooling.md).

Rules of thumb that usually matter:

- Find directions on one prompt set and measure them on another; otherwise the measurement rewards overfitting to the prompts.
- Every effect sits next to a matched control of the same size (k random directions, same-norm steering, a random-init model), so "we removed a lot" is not mistaken for "we removed the right thing".
- Work on a small model until the pipeline and the controls behave, then scale; many interp bugs look like findings.
- Use float32 for Jacobians and SVDs, and log the actual token at each position you study.

## Tools

Plain torch forward hooks are the default: they work on any Hugging Face causal LM and are easy to read. Reach for nnsight when a model is too big to run yourself (NDIF), TransformerLens when its hooked model and utilities fit the architecture, pyvene for interchange interventions and DAS, and SAELens for pretrained SAEs. [Tooling](references/tooling.md) has verified loading snippets and the version traps.

## With a lab

When a lab is present, start from `lab new exp <name> --template interp` and use `from lab import interp` (`load`, `blocks`, `resid`, `jacobian`, `spectrum`, `random_basis`, `ablate`, `next_token_loss`, `sae_basis`, `bootstrap`) rather than writing new hooks. Put prompt and eval sets in `locked/`, log spectra with `fig.line(log_y=True)`, bases against controls with `fig.dots`, per-token readouts with `fig.tokens`, and layer-by-position patching with `fig.heatmap`. Scale with `lab run -- modal run -m lab.modal_app --script experiment.py --gpu A100-80GB`. [Experiment shapes](references/experiment-shapes.md) lays out a campaign.
