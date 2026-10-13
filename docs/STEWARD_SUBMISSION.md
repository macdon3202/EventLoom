# EventLoom submission

Contribution date: 2026-10-13

Title: EventLoom — AI-Assisted Indexer Event Compatibility Registry

## Notes / Description

Built EventLoom V2, a contract-only GenLayer application that evaluates event-interface compatibility between two verified ABI snapshots from fixed Blockscout origins. Deterministic checks enforce event name, parameter types, order, indexed flags and non-anonymous mode. AI may identify semantic renames, but these return ADAPTER_REQUIRED rather than claiming existing indexer compatibility. Missing, ambiguous or unverified evidence cannot produce COMPATIBLE.

The deployer has no runtime privilege. Two auxiliary wallets ran 13 finalized StudioNet transactions: an exact-interface COMPATIBLE case, source/semantic uncertainty cases, and five expected permission/replay/duplicate rejections with complete state rollback. Local verification passed 33 tests plus GenVM lint and validation. Anonymous-event and rename fixes are covered by local regressions; those branches are not claimed as direct live outcomes.

## Evidence links

- [Repository](https://github.com/macdon3202/EventLoom)
- [Current V2 E2E entry point](https://github.com/macdon3202/EventLoom/blob/main/docs/STUDIONET_E2E_V2.md)
- [V2 audit transaction links and rollback evidence](https://github.com/macdon3202/EventLoom/blob/main/docs/LIVE_AUDIT_V2.md)
- [V2 deployed contract](https://explorer-studio.genlayer.com/address/0xF1328d04f45f2aC59dd212c8687897d54288C719)
- [Current contract source](https://github.com/macdon3202/EventLoom/blob/main/contracts/event_loom.py)
- [Proof obligation](https://github.com/macdon3202/EventLoom/blob/main/docs/PROOF_OBLIGATION.md)
- [Test-source manifest](https://github.com/macdon3202/EventLoom/blob/main/docs/TEST_RESOURCE_MANIFEST.md)

The V1 files are historical audit evidence. The submitted deployment is V2.
