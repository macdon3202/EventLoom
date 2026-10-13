# Test-resource manifest

## Admissible live sources

A live compatibility claim must use public, stable, verified smart-contract
pages from the exact Blockscout origins hard-coded in the contract. Locally
hosted JSON, mutable gists, custom proxies and test pages are not authoritative.

For every old/new pair, evidence must record:

- chain key and both exact API/page URLs;
- both contract addresses and verification state;
- normalized ABI snapshot digests returned by EventLoom;
- the exact obligation JSON;
- why the pair is expected to be compatible, breaking or unresolved;
- auxiliary creator/evaluator addresses;
- StudioNet create/evaluate transaction hashes; and
- final `get_dossier` readback.

## Local fixtures

Fixtures in `tests/test_event_loom.py` exist only to exercise deterministic and
adversarial branches. They must never be cited as evidence of a real external
contract.

## Role rule

The deployment wallet must not appear as dossier creator or evaluator. Wallet A
creates; wallet B evaluates. Reviewer-owned wallets must also be able to use the
same permissionless flow.

## Audited live candidate (2026-10-13)

The following Optimism pair was checked directly against the fixed API and is a
suitable `COMPATIBLE` fixture:

- Old: WETH9 `0x4200000000000000000000000000000000000006`
- New: USDT `0x94b008aA00579c1307B0EF2c499aD98a8ce58e58`
- Required event: `Transfer(address indexed,address indexed,uint256)`
- Both endpoints reported `is_verified = true`.
- Both ABIs expose the exact required parameter types, order and indexed flags.

This is a compatibility test fixture, not a claim that WETH migrated to USDT.
The migration reference must explicitly identify it as an interface-compatibility
demonstration. Live evidence is still pending a deployed EventLoom address.
