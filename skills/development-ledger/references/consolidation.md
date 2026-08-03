# Consolidation phase

Turn accumulated observations into a smaller, stronger current model.

## Consolidation loop

1. Triage each inbox item as duplicate, durable finding, question, proposal, or irrelevant.
2. Merge duplicates around one precise claim and retain the strongest evidence.
3. Promote durable claims into Consolidated Findings.
4. Move unresolved uncertainty into `03-questions.md`.
5. Rewrite `04-synthesis.md` from the surviving findings; do not append competing summaries.
6. Move adopted choices to `05-decisions.md` and reduce superseded choices to brief history entries.
7. Clear processed inbox items.
8. Update `README.md` and its `Last consolidated` watermark.

## Conflict handling

- Prefer observed runtime behavior over comments or assumptions.
- Prefer canonical code paths and primary sources over summaries.
- Preserve conflicting evidence until resolved.
- Lower confidence when evidence is partial or stale.
- State what new observation would resolve the conflict.

## Compression policy

Retain claims, evidence pointers, implications, decisions, and unresolved questions. Remove raw transcripts, repeated explanations, abandoned speculation, and details recoverable directly from cited sources.

If a lifecycle file remains above 250 lines after consolidation, split only bulky supporting evidence into an adjacent appendix and link it. Keep the standard lifecycle files sufficient for re-entry.
