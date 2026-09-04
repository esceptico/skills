# Tool Harness Design Principles

Use this reference to reason about findings and durable fixes during a tool-harness audit. These are not universal mechanical rules; apply them according to ownership, semantics, and risk.

## 1. Model the agent’s decision surface

A harness is not merely a collection of backend endpoints. It is a decision surface presented to an agent.

For each user intent, ask:

- Which tool should the agent choose first?
- What information must it already know?
- What stable handle will support the next action?
- What user decision must remain explicit?
- What failures are predictable and recoverable?

If two tools appear equally plausible for the same intent, ownership is unclear even if their backend implementations differ.

## 2. Choose tool boundaries deliberately

### Split tools when

- the operations represent distinct user decisions;
- risk or authorization differs materially;
- one operation is destructive and another is exploratory;
- different owners or systems define the authoritative behavior;
- combining them would hide an important choice.

### Consolidate tools when

- the sequence is a mechanical read chain;
- intermediate results have no independent user value;
- exposing each backend hop increases tool-selection or reference errors;
- one bounded operation can return the information needed for the next decision.

A good pattern is often:

1. bounded discovery or proposal;
2. explicit consequential mutation;
3. observable verification.

Avoid both endpoint-shaped fragmentation and opaque mega-tools.

## 3. Make descriptions operational

State the intent the tool owns and the information needed to choose it correctly. Include exclusions, prerequisites, sequencing, or recovery guidance only when they prevent a likely mistake. Keep argument details in parameter schemas and continuation details in results when possible; avoid repeating them in every description.

## 4. Treat schemas as executable communication

Schemas should make valid calls easy and invalid calls difficult.

Prefer:

- narrow, unambiguous parameter names;
- enums for genuinely closed domains;
- explicit formats for time, email, paths, and identifiers;
- defaults only when they reflect a safe, stable common case;
- documented conditional requirements;
- deterministic ordering where order matters.

Avoid:

- generic `id`, `value`, `data`, or `payload` fields when a semantic name exists;
- permissive blobs that move validation into prompting;
- misleading optional fields that are actually required in common states;
- provider-specific constructs without verifying provider behavior.

## 5. Validate at the authoritative boundary

Validation should exist where invalid input can still cause harm or ambiguous execution.

Do not duplicate every validation rule at every layer automatically. First identify:

- the authoritative schema;
- transformations performed by the provider or adapter;
- the execution/trust boundary;
- whether remote integrations can bypass local guarantees.

Add host-side validation when raw JSON Schema, adapters, provider transformations, or remote execution weaken the authoritative guarantee.

## 6. Preserve optional-value semantics

`null`, omission, empty string, empty list, and empty object are not universally equivalent.

Normalize them only when the domain contract declares them equivalent. Preserve intentional `null` when it means something such as:

- clear the existing value;
- explicitly unknown;
- inherit from a parent;
- no assignee;
- unbounded range.

Blanket cleanup can silently change mutation semantics.

## 7. Design outputs for the next decision

Useful outputs answer:

- What happened?
- What matters?
- What stable reference can be used next?
- Is there more data?
- How can the agent narrow or continue?
- Where did a derived claim come from?

Prefer compact, stable, agent-readable results over raw backend dumps. Structured data may still be appropriate for chaining, but it should expose intentional fields rather than incidental internals.

## 8. Bound large reads

Large reads should provide:

- safe defaults;
- explicit limits;
- stable cursors or continuation tokens;
- truncation indicators;
- total or estimated counts where available;
- narrowing guidance;
- deterministic sort order.

Do not silently truncate without telling the caller. Do not return an unbounded result merely because the backend permits it.

## 9. Use semantic and stable references

Prefer names, paths, handles, emails, slugs, or stable tool-level references over raw storage identifiers.

Response-local index references are acceptable only when their scope is obvious and protected by a response token or equivalent mechanism. Do not imply an unstable index is globally reusable.

## 10. Make mutations proportionally safe

Risk controls should match the operation.

Possible controls include:

- preview or dry run;
- explicit confirmation;
- expected version / `if_match`;
- idempotency keys;
- natural no-op behavior;
- conflict detection;
- restricted scopes;
- reversible operations;
- changed-state returns;
- a follow-up verification path.

Do not impose a universal read-before-write rule. Some operations are safely idempotent or already contain sufficient context. Require a pre-read when it materially reduces stale-state, identity, scope, or consequence risk.

## 11. Make errors actionable

An actionable error states:

- what failed;
- which field or prerequisite caused it;
- whether retrying unchanged can work;
- the next tool or argument needed;
- whether the query must be narrowed;
- whether authorization or reauthentication is required;
- whether partial state changed.

Avoid returning only transport codes or generic exceptions.

## 12. Separate deterministic and stochastic evidence

Deterministic tests can establish:

- schema generation;
- validator behavior;
- formatter behavior;
- pagination invariants;
- idempotency and conflict handling;
- stable ordering;
- error mapping.

Agentic evaluations are needed to establish:

- correct tool selection;
- argument generation across paraphrases;
- recovery after failure;
- effective use of continuation guidance;
- workflow completion under realistic context.

A single successful stochastic run is an example, not a reliability estimate.

## 13. Evaluate workflows and cohorts

Tool-by-tool review alone misses composition failures. Evaluate representative workflows such as search → inspect → preview → mutate → verify.

For large harnesses:

- catalog the complete tool population where practical;
- group tools by shared contract path;
- deeply review risk- and usage-selected representatives;
- record cohort sizes and reviewed counts;
- identify exceptions and uncovered areas;
- avoid implying sampled evidence equals complete runtime coverage.

## 14. Keep causal claims proportional to evidence

Runtime failure does not by itself identify the responsible layer. Compare:

- source schema;
- generated catalog;
- provider-visible schema;
- actual call arguments;
- host validation;
- remote/backend response;
- formatted tool result.

When evidence is incomplete, report a hypothesis and the experiment or instrumentation required to verify it.

## 15. Keep security claims separate

Agent ergonomics and reliability can expose security-relevant symptoms, but passing this audit does not establish secure authorization, tenant isolation, privacy, or abuse resistance.

If observed hazards need specialist investigation, identify that gap. Do not turn every production harness review into a separate security-audit requirement.
