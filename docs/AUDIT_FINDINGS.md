# V1 audit findings — 2026-10-13

Correction status: local V2 fixes are implemented and 33 tests pass. See
[V2_CHANGES.md](V2_CHANGES.md). The deployed V1 address remains unchanged.

Audit target: deployed `EVENT_LOOM_V1`, address
`0x1BEd25324D7F520433e84B51777Ee80d0Df9dBf0`.

## High: anonymous event can receive false COMPATIBLE

`normalize_events` preserves `anonymous` but `evaluate_sources` compares only
event names and input layout. A non-anonymous Transfer event changed to anonymous
passes the exact-event positive gate. This changes log topics and can break
indexer filters. Regression `test_anonymous_event_must_not_pass_topic_compatible`
reproduces the false positive against the unmodified V1 source.

Required correction: bind the baseline and new event anonymous mode in every
exact and semantic comparison; explicitly define supported baseline mode.

## High: semantic rename does not preserve existing topic filters

V1 classifies a renamed event with matching parameter layout as COMPATIBLE.
Renaming a non-anonymous event changes its signature and therefore topic0.
Semantic similarity alone cannot prove an existing indexer still works. A rename
needs a separate adapter-required standing, or a verified and sealed explicit
indexer remapping policy. V1 currently stores no such consumer policy.

Reference: [Solidity event documentation](https://docs.soliditylang.org/en/latest/contracts.html#events).

## Coverage and deployment implication

Expanded local run: 29 passed, 1 failed (anonymous-event regression).
The original 25 passing tests did not cover anonymous mode. They are insufficient
to declare V1 safe for general indexer compatibility submissions.

No deployed code was changed by this audit. Correcting these logic gates requires
a new deployment and fresh E2E evidence bound to the corrected source.

Live audit checkpoints, transaction links and before/after full readbacks are
saved incrementally in `live-audit.json` by `scripts/audit_live.py`.

## Completed live audit outcomes

- Terminal evaluation replay: expected error and full state unchanged.
- Unauthorized cancellation: `CREATOR_REQUIRED`, full state unchanged.
- Duplicate dossier: `DOSSIER_ALREADY_EXISTS`, counter and records unchanged.
- Creator evaluating a sealed dossier: `INDEPENDENT_EVALUATOR_REQUIRED`, full
  state unchanged.
- WETH Deposit obligation against USDT: `REVIEW_REQUIRED` with
  `SEMANTIC_EQUIVALENCE_UNKNOWN`. This is a completed uncertainty test, not a
  committed BREAKING result.
- WETH Transfer against verified NFT Position Manager: `REVIEW_REQUIRED`,
  `SOURCE_VERIFIED:SOURCE_INVALID`. The NFT endpoint body measured 248,928 bytes,
  exceeding V1's 220,000-byte bound. This is source-size rejection, not proof
  of the intended indexed-layout BREAKING branch.

All submitted audit transactions reached FINALIZED / MAJORITY_AGREE. Reverted
transactions were validated by their expected error and exact before/after
readbacks, not classified as successful writes.

## Remaining coverage boundaries

Confirmed BREAKING, semantic rename, forced network outage, malformed model and
validator disagreement are not established live by these runs. Local tests
cover the deterministic branches; transient fault injection must remain labelled
local rather than replacing authoritative live sources with fabricated pages.
