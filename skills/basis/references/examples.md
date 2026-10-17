# Applying the basis lens

These examples illustrate the method. They are not a universal architecture or current specifications for Arden.

## Agent updates: dimensions instead of named-case branches

A child reports while its parent may be writing, running a tool, idle, or finished. The update may be progress, a question, a success, or a failure. It may arrive live or be restored from history.

Useful distinctions include source identity, causal turn, recipient lifecycle, update kind, and delivery state. Test whether existing owners already provide them. Do not infer “currently running” from the existence of an old message, infer the initiator from its wording, or attach a late update to the most recent answer merely because it is nearby.

| Case | Required distinction |
| --- | --- |
| Idle parent receives a stored message | Arrival does not itself imply activity or an answer. |
| Active parent receives progress during a tool call | Incoming information does not itself settle the tool or split a human turn. |
| Child succeeds while parent stays silent | If the product promises result visibility, the result needs an inspectable presentation. |
| Parent explains the result | Presentation can prioritize that explanation while preserving promised access to the underlying result. |
| History is restored after restart | Historical activity must not become current activity. |

One interpretation of canonical events can feed several presentations. That is different from building a renderer branch for every combination. Terminal states that cannot produce new tool calls should be excluded from that product; a queued message from before termination is a different, valid sequence.

## Continuity: shared evidence does not mean one state

A timeline, summary, unread badge, and unresolved question may all refer to the same work. Their responsibilities differ:

- Evidence says what happened, with identity and time.
- Understanding says what currently holds, with sources and freshness.
- Attention says what needs action or has not been seen, for a particular reader.

These labels were useful in an Arden discussion; another domain may need different ones. Even here, “attention” does not imply a single boolean or cursor. Reading a question, resolving it, delivering a notification, and an agent reviewing its source are different acknowledgements.

A timeline can project existing records instead of copying them into a second authoritative journal. A shared reader is useful if its contract preserves scope, revisions, and coverage. Merging every checkpoint into `processed` loses meaning.

## A holistic fix can remain small

Suppose a badge and list disagree about open questions. Trace both to their data and eligibility decisions. If they mean the same thing, repair or reuse the owning predicate and update the consumers. If one represents unseen history and the other unresolved action, preserve the distinction and make their meanings clear.

Do not fix the badge with title matching, hide the discrepancy in one component, or introduce a universal attention framework without a demonstrated need. The breadth belongs in tracing the affected contract; the implementation may be one small correction.

## Distinct concerns can stay in one controller

A save controller already owns request state and exposes errors, but a failed save leaves its retry button disabled because cleanup runs only on success. Correct the existing completion path and check success and failure. Inspect overlapping requests only if the controller supports them.

Loading, error presentation, and retry eligibility have distinct meanings. That distinction does not require separate services or interfaces. The repair can add no abstraction and need no written matrix.
