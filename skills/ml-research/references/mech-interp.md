# Mechanistic Interpretability Evidence Pattern

Use this reference for circuits, activation patching, causal tracing, attribution, probes, sparse autoencoders, transcoders, steering, ablation, representation geometry, and other model-internals research.

## Core evidence unit

`model/component + interpretability method + intervention → measured effect`

Do not call a discovered correlation a causal mechanism.

## Evidence to inspect

Select checks that bear on the claim. Descriptive research need not establish causality, but a causal conclusion needs intervention evidence and suitable controls.

### Target

- Model and exact checkpoint
- Layer, hook point, head, MLP, residual stream, feature, direction, or circuit
- Behavior, token, task, prompt distribution, or capability being explained

### Method and claim

- Interpretability method and component/feature selection procedure
- Normalization, baselines, thresholds, and aggregation
- Precise proposed representation or mechanism
- Whether examples and hypotheses were selected exploratorily or evaluated on held-out data

### Evidence

- Activation statistics or feature examples
- Quantitative faithfulness, completeness, or reconstruction metrics
- Logit, loss, accuracy, generation, or behavioral measurement
- Circuit or feature coverage

### Intervention and effect

- What was patched, ablated, clamped, steered, or replaced
- Source and destination condition, location, and magnitude
- Exact effect relative to a baseline
- Persistence across prompts, tasks, layers, checkpoints, or models

### Controls

Check for:

- random components or directions;
- resampling or corrupted baselines;
- matched-norm interventions;
- alternate layers, models, prompts, and tasks;
- held-out examples;
- multiple seeds or uncertainty;
- tests against probe or feature-selection artifacts.

### Artifacts and limitations

Use [artifact verification](artifact-verification.md) for exact model, SAE/transcoder, activation dataset, dashboard, code, and evaluation-script identifiers and revisions. Assess feature splitting and absorption, polysemanticity, reconstruction loss, downstream loss recovery, cherry-picked examples, prompt sensitivity, and external validity.

## Interpret causal evidence along separate dimensions

Descriptive examples, predictive probes, and attribution can motivate a mechanism without establishing it. Assess each relevant dimension separately rather than assigning a single causal-strength rank:

- **Necessity:** does removing or replacing the component impair the behavior under the tested conditions? Redundant mechanisms can mask necessity; broad damage can mimic it.
- **Sufficiency:** does introducing or restoring the component produce or recover the behavior in the tested background? This does not establish that the intact model normally uses that route.
- **Specificity:** do matched controls distinguish the proposed mechanism from generic disruption or another explanation?
- **Generalization:** does the claim survive held-out prompts, distributions, or models? Replication of an effect alone does not establish its mechanism.

For patching, record source/destination conditions, direction, corruption method, magnitude, and metric. Explain what the intervention tests in that setup; patching directions are not interchangeable. Check whether an intervention creates off-distribution activations or broad performance degradation. A behavioral change alone does not distinguish disruption from the claimed mechanism.

Report supported and unresolved dimensions independently. Distinguish intervention effects in a surrogate or reconstructed model from evidence about the original model, and inspect fidelity when transferring that conclusion.

## Recommendation gate

Before accepting a mechanistic claim, answer:

1. What exact behavior is explained?
2. What intervention changes it?
3. Which controls rule out simpler explanations?
4. How much of the behavior is explained?
5. Does the effect generalize beyond selected examples?
6. Are the model, activations/features, and evaluation code reproducible?

Prefer a small held-out causal test with a matched random or matched-norm control. Measure both the target behavioral effect and collateral degradation. When assessing SAE fidelity or intervention results, inspect reconstruction, loss recovery, sparsity, dead features, and intervention specificity as relevant. Distinguish reported metrics from unavailable ones.
