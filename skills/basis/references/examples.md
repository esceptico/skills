# Applying the basis lens

Each example has the same shape: the situation, the tempting move, the basis move, and the responsibility test that decides it. The domains are illustrative, not specifications.

## A case exposes a missing dimension

**Situation.** An order system branches on `status` (placed, paid, shipped, delivered, cancelled) and `action` (cancel, refund, reship). A support ticket: a customer cancelled after the shipping label printed but before carrier pickup, and the order shows "cancelled" while the parcel still ships.

**Tempting move.** Add a rule for "cancelled after label, before pickup".

**Basis move.** The case shows that `status` was standing in for two facts: the commercial state of the order and the physical state of fulfilment. They change independently, so they are two dimensions. Rebuild the rows on both:

| State/context + event | Expected transition and user outcome | Current behavior/evidence | Owning contract |
| --- | --- | --- | --- |
| paid, label printed + cancel | Order cancelled; label voided; customer told nothing shipped | Order cancelled; label untouched (ticket #4812) | Order owns commercial state; Fulfilment owns label and must observe cancellation |
| paid, picked up + cancel | Cancellation becomes a return; customer told to refuse or return | Same path as above, parcel in transit | Fulfilment: picked-up parcels cannot be voided; Returns owns the rest |
| placed, unpaid + refund | Unreachable: nothing to refund | Not guarded; refund handler throws | Exclude by the invariant "refund requires a captured payment" |

**Test.** Commercial state and fulfilment state can each change while the other stays fixed, so they are two responsibilities. The unreachable row is excluded by its invariant, not by a special case in the handler.

## Shared evidence does not mean one state

**Situation.** A project workspace shows an activity log, a current-status summary, an unread badge, and a list of open questions. All four describe the same underlying events.

**Tempting move.** One `processed` cursor per user: everything before it is seen, resolved, and summarised.

**Basis move.** Three responsibilities with different owners and lifecycles:

- Evidence: what happened, with identity and time. Append-only.
- Understanding: what currently holds, with sources and freshness. Recomputed or revised.
- Attention: what a particular reader has not seen or still has to act on. Per reader, with distinct acknowledgements.

The log, summary and badge are projections of these, not copies. Within attention, "read the question", "resolved it", "notification delivered" and "agent reviewed its source" are separate facts; collapsing them into one cursor loses the ability to answer "was this seen but left open?".

**Test.** A question can be read without being resolved, and resolved without being read by everyone. Either changes alone, so they are not one state.

## A background task reports into a conversation

**Situation.** A worker posts progress, questions, successes and failures into a thread. The reader may be active in the thread, busy elsewhere, idle, or disconnected. Reports may arrive live or be restored from history after a restart.

**Tempting move.** A renderer branch per combination of reader state and report kind.

**Basis move.** Identify the distinctions that change the outcome: who sent it, which turn caused it, the reader's current lifecycle, the report kind, and whether this is a live arrival or a replay. Check whether existing owners already provide each; usually the message store knows the sender and causal turn, and the session knows the lifecycle. Then one interpretation of the canonical events feeds every presentation.

Guards the cases impose:

- A stored report arriving at an idle reader does not make the reader active, and does not count as an answer.
- Progress arriving mid tool-call does not settle the tool or split the human's turn.
- A replayed history must not become current activity.
- If the product promises that results are inspectable, a quiet presentation still has to expose the result somewhere.

**Test.** Reader lifecycle and report kind change independently, so they are separate dimensions, but neither is a new owner. The repair is a single interpreter over existing facts, not a matrix of renderers.

## A holistic fix can remain small

**Situation.** A badge says 3 open questions; the list below it shows 2.

**Tempting move.** Make the badge count the list's rows, or match titles until the numbers agree.

**Basis move.** Trace both to their data and eligibility decisions. Two outcomes are possible:

- They mean the same thing. Then one predicate owns "open question", both consumers call it, and the fix is a few lines.
- They mean different things, say unseen history versus unresolved action. Then preserve the distinction and label each so the reader understands why they differ.

**Test.** If one count can change while the other does not, they are two facts and should not be forced to agree.

## Sharing a predicate without changing its meaning

**Situation.** Overdue-invoice eligibility is computed in three places. A change to the grace period has to land in all of them.

**Tempting move.** Replace all three with one query over every invoice.

**Basis move.** Consolidate the eligibility rule at one owner, but keep each caller's scope: the customer page selects that customer's invoices, the dispute queue excludes disputed ones, the nightly job counts in invoices while the dashboard counts in customers. A shared reader whose contract preserves the selected entities and the count unit is a consolidation; one that widens every caller to "all records" changes their meaning while keeping their numbers plausible.

**Test.** The grace-period rule changes for one reason, so it is one responsibility. Each caller's scope changes for its own reasons, so scope stays with the caller.

## Distinct concerns can stay in one controller

**Situation.** A save controller already owns request state and exposes errors, but after a failed save the retry button stays disabled, because the cleanup that re-enables it runs only on success.

**Tempting move.** Separate loading, error and retry into their own services or a state machine.

**Basis move.** Correct the completion path so cleanup runs on both outcomes; check success and failure. Inspect overlapping requests only if the controller supports them.

**Test.** Loading, error presentation and retry eligibility have distinct meanings, and the test says they are distinct responsibilities. That does not require distinct code structure; a responsibility is a reasoning boundary. Here the complete repair adds no abstraction and needs no written matrix.
