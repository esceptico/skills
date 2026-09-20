# Evaluation Notes

## History

- **1.x (evaluated August 28, 2026).** Three one-shot literature scenarios. The skill improved mechanistic-interpretability reasoning and artifact verification, and a dated current-artifact scan fixed anchoring on old checkpoints. Splitting standard ML and mech interp into references kept the benefits while shrinking `SKILL.md`.
- **2.0 (September 20, 2026).** Rewritten after agents using 1.x behaved narrowly: they answered the literal question, did one paper check, and stopped. Cause: the skill was a review skill (evidence units, comparability gates) with no research loop, no hygiene ladder, no log, no stopping or scale-up rules, and evals that only asked literature questions. Sources for the rewrite: Neel Nanda's research-process sequence, Karpathy's training recipe and autoresearch loop, Prime Intellect's agent conventions, Cognition's Kevin-32B loop and playbook shape, the AutoResearch failure taxonomy (arXiv 2608.14905). Evals 1 and 2 are now campaigns with a metric and a sandbox; 3 and 4 keep the literature scenarios.

## Scenarios

1. Fixed-budget val_bpb campaign on a nanoGPT-style repo (autoresearch shape).
2. A narrow "does X help" question that should open into a loop with hygiene checks.
3. Model and method selection under a compute constraint, plan only.
4. Causal-versus-correlational assessment of Gemma SAE evidence.

## Open

- 2.0 has not yet been run against these scenarios. Run 1 and 2 first; they are the ones 1.x could not do.
- Reconsider a bundled log-table script only if runs repeatedly hand-build the same table.
