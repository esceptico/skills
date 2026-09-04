# Agentic evaluations

Use when testing model tool selection, argument generation, chaining, or recovery. Static review alone cannot establish these behaviors.

Choose realistic tasks from the audited scope, including relevant failures such as no results, pagination, stale references, conflicts, or interrupted mutations. Define acceptance criteria before running them. Use authorized fixtures or environments; an audit request alone does not authorize consequential live writes.

## Outcomes and discovery

Grade the resulting state against the user's requested outcome using an independent fixture assertion, readback, or artifact inspection where possible. Valid arguments, a success response, or a persuasive final answer do not establish task success. If final state is unobservable, state that limit.

Include applicable cases where success means no tool call, clarification, or stopping after an unresolved outcome. Judge whether the action was appropriate, not whether the agent followed one prescribed call sequence.

Exercise discovery with the catalog and competing tools actually available in the target environment. When supported, include lazy discovery and continuation after earlier results leave context. Check whether the agent can recover prerequisites and references without guessing identifiers or repeating completed writes. Avoid handing the evaluator the intended tool name unless users would supply it.

## Comparisons and evidence

Compare harness revisions on the same tasks, starting fixtures, model configuration, and budgets. Reset mutable fixtures between trials; use held-out tasks when tuning descriptions against an evaluation set. Record unavoidable differences and avoid attributing their effects to the harness change.

Record the task, model/version, provider and tool-calling configuration, harness/schema revision, state, and relevant permission assumptions. Measure completion and the costs relevant to the claim: invalid arguments, wrong tools, retries, calls, latency, context use, truncation, or failed mutation verification.

Report run counts and successes/attempts. Use repeated runs when estimating reliability; a single run is an example. Choose repetition based on the uncertainty and cost rather than a fixed quota. Keep representative failures and state the limits of generalization.

Trace failures through the available evidence: source schema, provider-visible schema, generated arguments, execution validation, backend response, and formatted result. Label an unverified cause as a hypothesis and identify the evidence that would distinguish competing explanations.
