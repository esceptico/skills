# Evaluation Notes

Evaluated on August 28, 2026.

## Scenarios

1. Select and adapt a current open 7B–9B model for 32k-document instruction following under a one-week, 4× H100 constraint.
2. Assess whether Gemma-family sparse-autoencoder evidence is correlational or causal and propose a discriminating intervention.
3. Select a reproducible open-source RAG hallucination-detection baseline and verify its model, data, code, licenses, APIs, and smoke test.

## Findings

- The original one-file skill improved mechanistic-interpretability reasoning and artifact verification, but its standard-ML run anchored on an older checkpoint.
- Splitting standard ML and mechanistic interpretability into references preserved those benefits while reducing `SKILL.md` from 213 lines to about 70.
- Generic freshness language was insufficient. The final skill requires searching official Hugging Face repositories by both creation and modification date, comparing at least three eligible finalists, and recording acceptance/rejection reasons.
- The regression rerun surfaced `Qwen/Qwen3.5-9B`, `ibm-granite/granite-4.2-8b`, `swiss-ai/Apertus-v1.5-8B`, and `meta-llama/Llama-3.1-8B-Instruct`, then selected Qwen3.5 with explicit evidence and caveats.
- Each revised run loaded only the directly relevant reference.
- No evaluation demonstrated repeated deterministic work that justified a bundled script. Reconsider a narrow evidence validator only if future runs repeatedly lose provenance or recreate the same validation logic.
