---
name: ml-research
description: Review ML research or select methods, models, and datasets using primary evidence; assess causal claims in mechanistic interpretability.
metadata:
  version: "1.2.0"
---

# ML Research

Answer the user's research decision with primary evidence. Keep reported results, inference, and recommendations distinct.

## Choose relevant guidance

- For model/data selection, training, inference, or benchmark comparisons, use [standard ML](references/standard-ml.md).
- For model-internals or causal-mechanism claims, use [mechanistic interpretability](references/mech-interp.md).
- Load both only when the question needs both evidence patterns. A narrow paper question needs only the relevant checks.
- When designing or running experiments, consult [experiment design](references/experiment-design.md).

## Evidence standard

Read the primary source sections supporting material claims; abstracts and snippets support discovery, not detailed conclusions. Keep each result tied to its model/checkpoint, data, metric, baseline, and evaluation conditions. Surface consequential contradictions and limits on transfer to the user's setting.

For contemporary recommendations, check recent eligible releases rather than anchoring on familiar work. Use the current-artifact scan in the standard ML reference when selecting artifacts, and report the evidence cutoff.

Verify the artifacts needed for the recommendation: exact repository/checkpoint IDs, licenses, relevant data splits and schema, and implementation/config files. Hugging Face Hub tools are useful for hosted artifacts; official repositories, APIs, or documentation are alternatives. Report [verification depth](references/artifact-verification.md) per artifact; an existing repository is not a reproduced result. A particular connector is not a prerequisite.

## Deliver and continue

Lead with the answer, then the decisive evidence and caveats. Include exact implementation references when useful. Recommend a discriminating experiment when uncertainty materially affects the decision; do not attach an experiment plan to every paper explanation.

Research-only requests end with the requested synthesis or plan. When implementation or experiments are already authorized, continue within that scope and budget through relevant verification. A research recommendation alone does not authorize paid compute or training.

Completion means the requested decision is answered, material claims are supported, and missing evidence is explicit. Use the format and depth the question needs rather than a fixed report structure.
