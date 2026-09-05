# Assessment labels

Use these labels when reporting workflow outcomes and findings.


Keep outcome, confidence, and severity distinct. These labels are defaults; use the project's vocabulary when it preserves those distinctions.

### Outcome

- **Pass** — the workflow completes correctly without material ergonomic or reliability costs.
- **Degraded** — the workflow completes, but with material costs such as retries, excess context, ambiguity, truncation, fragile recovery, or unnecessary tool calls.
- **Fail** — the workflow does not complete correctly or creates an unacceptable mutation/reliability risk.
- **Not tested** — no valid execution evidence was collected.

### Confidence

- **High** — reproducible runtime evidence or deterministic code/test evidence directly establishes the claim.
- **Medium** — multiple evidence sources strongly implicate the claim, but direct reproduction is incomplete.
- **Low** — limited, indirect, ambiguous, or non-reproducible evidence.

Low-confidence findings may still be potentially high severity. Label causal claims as hypotheses until verified.

### Severity

Apply severity to findings, not workflows:

- **High** — likely wrong-tool selection, unsafe writes, data loss, authorization-sensitive mistakes, or unrecoverable task failure.
- **Medium** — meaningful reliability, context, latency, or recovery cost.
- **Low** — localized consistency, naming, documentation, or polish issue.
