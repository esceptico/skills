# Verification phase

Use `07-verification.md` only for observed proof, failures, and accepted gaps.

## Evidence contract

For each verification item, record:

- Stable ID such as `V-01`
- Related implementation IDs
- Command, inspection, or scenario
- Expected result
- Observed result
- Result: `pass`, `fail`, `blocked`, or `not-run`
- Timestamp and evidence pointer

Prefer the smallest test that proves the contract, then run broader regression checks proportional to risk. Visual behavior requires rendered or interactive inspection when feasible; static source inspection alone is not visual proof.

## Completion rule

Set ledger status to `complete` only when:

- Every required verification item is `pass`; or
- Remaining failures or gaps are explicitly documented and the user accepts them.

An implementation checkbox, test command without captured outcome, or agent assertion is not proof.
