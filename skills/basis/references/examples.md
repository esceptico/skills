# Basis examples

Each example has four parts: the situation, the tempting move, the basis move, and the test that decides it. The test is the responsibility test, or the structure test when the question is about code shape. The domains are illustrations, not specifications.

## A case shows a missing dimension

**Situation.** An order system branches on `status` (placed, paid, shipped, delivered, cancelled) and `action` (cancel, refund, reship). A support ticket reports that a customer cancelled after the shipping label printed but before carrier pickup. The order shows "cancelled" and the parcel still ships.

**Tempting move.** Add a rule for "cancelled after label, before pickup".

**Basis move.** The case shows that `status` held two facts: the commercial state of the order and the physical state of fulfilment. They change independently, so they are two dimensions. Write the rows on both:

| State/context + event | Expected transition and user outcome | Current behavior/evidence | Owning contract |
| --- | --- | --- | --- |
| paid, label printed + cancel | Order cancelled, label voided, customer told nothing shipped | Order cancelled, label untouched (ticket #4812) | Order owns commercial state. Fulfilment owns the label and must observe cancellation |
| paid, picked up + cancel | Cancellation becomes a return, customer told to refuse or return | Same path as above, parcel in transit | Fulfilment cannot void a picked-up parcel. Returns owns the rest |
| placed, unpaid + refund | Rejected. Refund is not offered, and a direct request gets "no captured payment" | Refund is offered and the handler throws | Payments owns the invariant "refund requires a captured payment" |

**Test.** Commercial state and fulfilment state can each change while the other stays fixed, so they are two responsibilities. A user can still request the refund row, so it is reachable and stays in the matrix. Its outcome is a rejection by the invariant at its owner. It is not a special case for one status in the handler.

**Siblings.** The ticket named one cell. The same event in the next fulfilment state, picked up + cancel, fails the same way. Fix it in the same change.

## Shared evidence does not mean one state

**Situation.** A project workspace shows an activity log, a current-status summary, an unread badge, and a list of open questions. All four describe the same events.

**Tempting move.** One `processed` cursor per user. Everything before it counts as seen, resolved, and summarised.

**Basis move.** Three responsibilities with different owners and lifecycles:

- Evidence is what happened, with identity and time. It is append-only.
- Understanding is what holds now, with sources and freshness. The system recomputes or revises it.
- Attention is what one reader has not seen or still has to act on. It is per reader, with separate acknowledgements.

The log, the summary and the badge are projections of these, not copies. Inside attention, "read the question", "resolved it", "notification delivered" and "agent reviewed its source" are separate facts. One cursor for all of them cannot answer "was this seen but left open?".

**Test.** A reader can read a question without resolving it, and can resolve it before every reader has read it. Each fact changes alone, so they are not one state.

## A background task reports into a conversation

**Situation.** A worker posts progress, questions, successes and failures into a thread. The reader can be active in the thread, busy elsewhere, idle, or disconnected. A report can arrive live or come back from history after a restart.

**Tempting move.** One renderer branch for each combination of reader state and report kind.

**Basis move.** Find the distinctions that change the outcome. Here they are the sender, the turn that caused the report, the reader's lifecycle, the report kind, and live arrival or replay. Check which existing owner already has each fact. Usually the message store knows the sender and the causal turn, and the session knows the lifecycle. Then one interpretation of the canonical events feeds every presentation.

The cases require these guards:

- A stored report that arrives at an idle reader does not make the reader active, and does not count as an answer.
- Progress that arrives during a tool call does not settle the tool or split the human's turn.
- Replayed history does not become current activity.
- If the product promises that results are inspectable, a quiet presentation still shows the result somewhere.

**Test.** Reader lifecycle and report kind change independently, so they are separate dimensions. Neither needs a new owner. The repair is one interpreter over existing facts, not a matrix of renderers.

## A holistic fix can stay small

**Situation.** A badge says 3 open questions. The list below it shows 2.

**Tempting move.** Make the badge count the list's rows, or match titles until the numbers agree.

**Basis move.** Trace both numbers to their data and eligibility decisions. There are two possible results:

- They mean the same thing. Then one predicate owns "open question", both consumers call it, and the fix is a few lines.
- They mean different things, for example unseen history and unresolved action. Then keep both, and label each so the reader knows why they differ.

**Test.** If one count can change while the other does not, they are two facts. Do not force them to agree.

## Sharing a predicate without changing its meaning

**Situation.** Three places compute overdue-invoice eligibility. A change to the grace period has to go into all three.

**Tempting move.** Replace all three with one query over every invoice.

**Basis move.** Move the eligibility rule to one owner, and keep each caller's scope. The customer page selects that customer's invoices. The dispute queue excludes disputed invoices. The nightly job counts invoices and the dashboard counts customers. A shared reader that keeps each caller's selected entities and count unit is a correct merge. A shared reader that widens every caller to "all records" changes what each number means, and the numbers still look plausible.

**Test.** The grace-period rule changes for one reason, so it is one responsibility. Each caller's scope changes for its own reasons, so scope stays with the caller.

## Distinct concerns can stay in one controller

**Situation.** A save controller already owns request state and exposes errors. After a failed save the retry button stays disabled, because the cleanup that enables it runs only on success.

**Tempting move.** Split loading, error and retry into their own services or a state machine.

**Basis move.** Correct the completion path so cleanup runs on both outcomes. Check success and failure. Check overlapping requests only if the controller supports them.

**Test.** Loading, error presentation and retry eligibility have different meanings, so the responsibility test says they are separate responsibilities. The structure test then asks if any of them needs its own code. No second place decides any of them, none has a second caller, and all share the controller's lifecycle. They stay in the controller. The complete repair adds no abstraction and needs no written matrix.

## Share the stateless part, keep the lifecycles apart

**Situation.** A live stream client and a history loader both turn the same wire format into messages. The stream reconnects and resumes. The loader pages through a file once. Each has its own copy of the parsing code, and a new field went into only one copy.

**Tempting move.** One client class with a `mode` flag that handles both streaming and paging.

**Basis move.** Move the parsing into one stateless function that both call. Leave connection, resume and paging with their current owners.

**Test.** The wire format changes for one reason and two places decode it, so it is one responsibility and it passes the structure test. Reconnect and paging change for their own reasons, so the lifecycles stay separate.
