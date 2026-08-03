---
name: tool-harness-audit
description: "Audit MCP and agent tool harnesses for agent ergonomics and reliability: tool discovery and selection, schemas, validation, outputs, pagination, references, errors, provenance, mutation safety, observability, recovery, and agentic evaluation. Use for reviewing an existing tool catalog or workflow, not for greenfield implementation or a comprehensive security/privacy audit."
---

# Tool Harness Audit

Audit an existing MCP or agent tool harness for whether an LLM agent can discover, choose, call, chain, and recover from tools correctly without unsafe mutations, unnecessary retries, or wasted context.

This skill is intentionally audit-focused. It can recommend changes and verification gates, but it is not a greenfield harness builder.

## Audit boundary

Evaluate:

- tool discovery and selection;
- tool boundaries and ownership;
- schema clarity and argument validity;
- validation at the authoritative execution boundary;
- output usefulness, bounds, and continuation paths;
- semantic handles and stable references;
- errors and recovery guidance;
- mutation safeguards, idempotency, and observability;
- provenance and temporal clarity;
- end-to-end workflow reliability;
- deterministic contract tests and stochastic agentic evaluations.

Do not claim this audit establishes:

- security or privacy assurance;
- authorization correctness;
- tenant isolation;
- threat-model completeness;
- compliance;
- abuse resistance.

Surface obvious hazards, but recommend a separate specialist security/privacy audit for production or sensitive harnesses.

## Assessment taxonomy

Use three separate dimensions. Do not substitute one for another.

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

Use **Critical** only if the audited organization already uses it and the evidence supports immediate, broad impact.

## Core principles

1. **One obvious owner per intent.** Avoid overlapping aliases and near-duplicate tools that force agents to guess.
2. **Boundaries follow decisions, risk, and ownership.** Do not mechanically mirror backend endpoints. Consolidate mechanical read chains when it reduces agent error without hiding a user decision.
3. **Descriptions teach use.** State when to use a tool, when not to, prerequisites, related tools, result shape, and likely failures.
4. **Semantic handles beat opaque IDs.** Prefer names, paths, slugs, handles, emails, or stable response-scoped references.
5. **Outputs serve the next action.** Return useful values, changed state, provenance, and continuation guidance—not raw backend dumps.
6. **Output is bounded by default.** Paginate, truncate, filter, or summarize large results and explain how to continue.
7. **Validation belongs at the authoritative boundary.** Avoid pointless duplication, but add host-side validation when adapters, provider transformations, raw JSON Schema, or remote execution can weaken guarantees.
8. **Optional-value semantics are intentional.** Normalize `null`, omission, and empty values only when they are semantically equivalent. Preserve domain-significant `null`.
9. **Mutation safeguards are proportional to risk.** Do not universally require a pre-read. Use preview, dry run, confirmation, version checks, idempotency, or conflict detection when the risk warrants them.
10. **Mutations are observable.** Return what changed and provide a verification path when the underlying system permits it.
11. **Errors support recovery.** Explain the invalid field, prerequisite, next call, narrowing strategy, retry conditions, or permission requirement.
12. **Ordering and time are explicit.** Use deterministic ordering and absolute ISO-8601 timestamps with time zones.
13. **Derived results carry provenance.** Include source, query/window, and derivation details sufficient to understand the claim.
14. **Agentic claims require agentic evidence.** Deterministic schema tests are necessary but do not prove model behavior.

Read [references/design-principles.md](references/design-principles.md) when assessing ambiguous boundaries or translating a finding into a durable fix.

## Audit workflow

### 1. Establish scope and constraints

Record:

- harness/repository revision;
- tool-catalog or schema revision;
- providers, adapters, and strict/tool-calling modes;
- execution contexts such as chat, automations, or background tasks;
- fixture versus live mutable state;
- permissions and environment assumptions without secrets;
- evidence window;
- mutation restrictions;
- unavailable systems and known blind spots.

Define an audit budget and stopping rule before deep review.

### 2. Catalog the complete harness

Catalog every tool where practical using manifests, generated schemas, source inspection, or scripts.

For each tool capture at least:

- name and declared intent;
- description and prerequisites;
- parameters, defaults, and conditional rules;
- output and continuation behavior;
- side-effect class;
- source/implementation boundary;
- related or overlapping tools;
- shared schema, adapter, validator, formatter, and provider path.

Complete catalog coverage does not mean every tool receives equal-depth manual review.

### 3. Define contract cohorts

Group tools that share material behavior, such as:

- schema-generation path;
- adapter/provider transformation;
- validator;
- output formatter;
- side-effect/risk class;
- pagination or reference mechanism.

Record:

- cohort selection criteria;
- total cohort size;
- representatives deeply reviewed;
- known exceptions checked;
- uncovered members or areas;
- why representative evidence is expected to generalize.

### 4. Select the deep-review sample

Prioritize:

- high-usage tools and workflows;
- destructive or consequential mutations;
- historically failing paths;
- overlapping or ambiguous tools;
- high-output reads;
- remote/provider-transformed schemas;
- representative ordinary reads;
- a long-tail sample to reduce usage bias.

State sampling limitations explicitly.

### 5. Map representative workflows

Audit workflows, not isolated schemas. Cover where applicable:

- discover/search → inspect;
- no-results → query repair;
- large result → narrow or paginate;
- read/preview → mutate → verify;
- failure → recovery;
- stale state → conflict handling;
- retry → idempotent or safely rejected behavior.

For each workflow define acceptance criteria before testing.

### 6. Inspect static contracts

Check:

- tool-name and description clarity;
- overlap and ownership;
- required versus optional fields;
- enum and format constraints;
- conditional requirements;
- handling of omitted, empty, and `null` values;
- provider/adapter transformations;
- execution-boundary validation;
- destructive/open-world annotations;
- output shape and bounds;
- error contract;
- mutation result and verification path.

Use deterministic schema, unit, and contract tests for deterministic claims.

### 7. Run agentic evaluations

Record for each evaluation:

- case/task identifier and expected behavior;
- model and version;
- provider and strict/tool-calling configuration;
- tool-schema or harness revision;
- fixture or live state;
- relevant environment and permission assumptions;
- run count;
- acceptance threshold;
- observed numerator/denominator;
- variance where meaningful;
- representative failures.

Measure where applicable:

- argument validity;
- wrong-tool or no-call rate;
- execution rejection rate;
- useful-value correctness;
- task completion;
- latency;
- tool-call count;
- token use/output size;
- truncation;
- recovery behavior;
- mutation verification.

Do not treat one successful stochastic run as sufficient evidence.

### 8. Trace failures to the responsible layer

Distinguish:

- tool-selection failure;
- model argument-generation failure;
- schema-generation defect;
- provider/adapter transformation;
- host validation gap;
- remote integration failure;
- backend/domain failure;
- result-formatting defect;
- instrumentation gap.

Do not turn an unverified causal theory into a product fix. State what evidence would discriminate between hypotheses.

### 9. Recommend the smallest durable fixes

Prefer fixes that:

- remove ambiguity across a cohort;
- strengthen the authoritative boundary;
- preserve domain semantics;
- reduce calls or context without hiding decisions;
- make writes observable and recoverable;
- add deterministic regression coverage;
- add repeated agentic evaluation for stochastic behavior.

Separate harness findings from unrelated backend or integration incidents.

### 10. Report coverage honestly

The final report must distinguish:

- complete catalog/static coverage;
- automatic checks;
- cohort-covered tools;
- directly tested tools/workflows;
- intentionally sampled-out areas;
- unavailable or untestable paths;
- security/privacy work outside this audit.

## Output

Use [assets/report-template.md](assets/report-template.md).

Default to headings, labeled fields, and bullet records. Markdown tables are optional and must never be required for a valid report. For large generated inventories, attach CSV or JSONL rather than asking an agent to construct a large table.

Keep the main report prioritized and decision-oriented. Put raw logs and exhaustive inventories in appendices or an evidence ledger.
