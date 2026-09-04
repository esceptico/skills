# Agentic evaluations

Use when testing model tool selection, argument generation, chaining, or recovery. Static review alone cannot establish these behaviors.

Choose realistic tasks from the audited scope, including relevant failures such as no results, pagination, stale references, conflicts, or interrupted mutations. Define acceptance criteria before running them. Use authorized fixtures or environments; an audit request alone does not authorize consequential live writes.

Record the task, model/version, provider and tool-calling configuration, harness/schema revision, state, and relevant permission assumptions. Measure completion and the costs relevant to the claim: invalid arguments, wrong tools, retries, calls, latency, context use, truncation, or failed mutation verification.

Report run counts and successes/attempts. Use repeated runs when estimating reliability; a single run is an example. Choose repetition based on the uncertainty and cost rather than a fixed quota. Keep representative failures and state the limits of generalization.

Trace failures through the available evidence: source schema, provider-visible schema, generated arguments, execution validation, backend response, and formatted result. Label an unverified cause as a hypothesis and identify the evidence that would distinguish competing explanations.
