---
name: tool-harness-audit
description: Audit an existing MCP or agent tool harness for tool-selection, contract, and workflow reliability. Use for harness reviews, not ordinary backend edits.
metadata:
  version: "1.0.0"
---

# Tool Harness Audit

Assess whether an agent can discover, call, chain, and recover from the tools in scope. Deliver prioritized, evidence-backed findings and the smallest durable fixes.

## Scope and evidence

Use the requested scope and available evidence to choose review depth. Record the harness revision, provider/adapter path, execution environment, and unavailable surfaces when they affect conclusions.

For a focused review, inspect the relevant tools and shared contract path. For a whole-harness review, catalog the tools where practical and group shared schema, validation, output, and risk behavior into cohorts. Review representative workflows and known exceptions; state which members were only covered by inference.

Trace material findings through the responsible layers: declared schema, generated/provider-visible contract, execution validation, backend behavior, and returned output. Separate source evidence, deterministic tests, and observed agent behavior. A runtime failure alone does not prove its cause.

## Load details as needed

- For contract checks or proposed fixes, consult the relevant sections of [design principles](references/design-principles.md): boundaries, descriptions, schemas, validation, optional values, outputs, pagination, references, mutations, and errors.
- For model-selection, chaining, or recovery experiments, read [evaluations](references/evaluations.md). Record untested behavior when execution is unavailable or outside scope.
- For outcome, confidence, and severity labels, use [assessment](references/assessment.md).
- For a broad audit report, adapt [the report template](assets/report-template.md). A focused review may use a short findings list.

## Decision boundaries

Audit permission covers inspection and tests within the authorized environment. It does not authorize consequential live mutations. Prefer fixtures for mutation and retry scenarios; use existing execution authorization where it applies.

Recommend changes in an audit-only task. If the user also requested fixes, continue through the scoped implementation and relevant verification without an extra review checkpoint.

This audit does not establish security, privacy, or authorization correctness. Report concrete hazards found within scope without expanding into a separate security audit.

## Completion

Finish when the requested surfaces have been assessed to the supported depth and the report identifies material findings, evidence, fixes, and coverage gaps. Distinguish directly tested, statically checked, cohort-inferred, sampled-out, and unavailable paths. Never report untested workflows as passing.

Keep the main report decision-oriented; attach raw logs or large inventories only when they support review.
