# Proof obligation

## Positive standing

`COMPATIBLE` for dossier `d` means:

1. both ABI documents came from contract-selected Blockscout origins;
2. both sources explicitly reported `is_verified = true`;
3. both ABI event sets passed size, shape and type normalization;
4. the baseline ABI contains exactly compatible layout for every sealed event
   obligation;
5. the baseline and new ABI both expose the exact non-anonymous event name,
   parameter types, order and `indexed` flags, preserving the signature topic; and
6. validator consensus agrees on both ABI digests and every consequential
   obligation result.

All obligations are mandatory. There is no score or partial-positive threshold.

## Deterministic and semantic boundary

AI can propose only a differently named semantic mapping. It cannot waive type,
order or indexing mismatches. A mapped name must exist in the normalized new
ABI, be non-anonymous, and its layout must deterministically equal the obligation.
Even then the standing is `ADAPTER_REQUIRED`, not `COMPATIBLE`, because renaming
changes the signature topic. This standing is not evidence that an adapter exists
or that the indexer works. Anonymous baseline events are unsupported and yield
`REVIEW_REQUIRED`; a same-name new anonymous event yields `BREAKING`.

## Non-claims

EventLoom does not establish that:

- either contract will emit an event in a particular execution;
- implementation behavior is equivalent;
- an upgrade was authorized or safe;
- a proxy implementation will remain unchanged;
- event consumers can decode non-ABI runtime data; or
- a migration occurred before or after any wall-clock deadline.

No GenLayer timestamp is used to manufacture real-world timing evidence.
