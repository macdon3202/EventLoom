# EventLoom

Current source: **EVENT_LOOM_V2**, locally verified with 33 passing tests.
V2 corrects anonymous-event handling and classifies semantic renames as
`ADAPTER_REQUIRED`. V2 deployment:
[0xF1328d04f45f2aC59dd212c8687897d54288C719](https://explorer-studio.genlayer.com/address/0xF1328d04f45f2aC59dd212c8687897d54288C719).
Current evidence: [STUDIONET_E2E_V2.md](docs/STUDIONET_E2E_V2.md).
See [V2 changes](docs/V2_CHANGES.md).

EventLoom is a contract-only GenLayer application that records whether a new
verified contract ABI preserves the event interface required by an indexer
migration.

It is intentionally narrow. It does not prove runtime event emission, bytecode
equivalence, upgrade authorization, business-logic safety or proposal approval.
It proves only compatibility between explicit event obligations and two exact,
normalized verified-ABI snapshots fetched from fixed Blockscout origins.

## Why GenLayer

Deterministic code handles exact event names, parameter types, ordering and
`indexed` flags. When a required event was renamed, validators may semantically
map the old event purpose to one differently named event; deterministic code
still requires the mapped event to exist and have exactly compatible layout.

`COMPATIBLE` requires every obligation to be `EXACT` with a non-anonymous event.
A semantic rename returns `ADAPTER_REQUIRED`, because the indexer's topic filter
must change. Unknown,
unverified, malformed, unavailable or validator-disputed evidence cannot become
positive.

## Architecture

```text
wallet A seals old/new addresses + explicit event obligations
                              ↓
wallet B requests independent evaluation
                              ↓
validators fetch two fixed-origin verified ABI objects
                              ↓
deterministic ABI normalization and exact compatibility checks
                              ↓
bounded AI rename mapping only for otherwise-missing event names
                              ↓
deterministic all-obligations positive gate
                              ↓
COMPATIBLE / ADAPTER_REQUIRED / BREAKING / REVIEW_REQUIRED
```

The architecture is `DUAL_ABI_OBLIGATION_COMPATIBILITY_LATTICE`. It is not a
transaction-disclosure ledger, escrow, permit, payout gate or admin registry.

## Roles

- Main wallet deploys only; no deployer or owner is stored.
- Auxiliary wallet A creates a dossier.
- Auxiliary wallet B evaluates it.
- Any reviewer may reproduce this with arbitrary wallets; there is no allowlist.

## Fixed sources

- `https://optimism.blockscout.com/api/v2/smart-contracts/{address}`
- `https://base.blockscout.com/api/v2/smart-contracts/{address}`

The current Blockscout response does not echo the requested address. EventLoom
therefore does not invent a returned-address check: object binding comes from
the internally constructed fixed-origin URL plus stored chain/address inputs and
the digest of the exact normalized ABI returned at that URL.

## Public methods

- `create_dossier(chain_key, old_contract, new_contract, migration_ref, event_obligations)`
- `evaluate_compatibility(dossier_id)`
- `cancel_dossier(dossier_id)`
- `get_dossier(dossier_id)`
- `get_config()`

## Verification

```powershell
py -3.12 -m pytest tests -q --tb=short -p no:cacheprovider
$env:PYTHONUTF8='1'; genvm-lint check contracts\event_loom.py
```

Current result: **33 tests passed**; lint and contract validation passed.

Historical V1 StudioNet deployment (does not contain the V2 fixes):
[0x1BEd25324D7F520433e84B51777Ee80d0Df9dBf0](https://explorer-studio.genlayer.com/address/0x1BEd25324D7F520433e84B51777Ee80d0Df9dBf0).
Live evidence: [STUDIONET_E2E.md](docs/STUDIONET_E2E.md).

Deploy `contracts/event_loom.py` with no constructor arguments. Do not use the
deployment wallet for the dossier lifecycle. After deployment, copy the example
fixture file, replace its placeholders with audited verified-contract sources,
and run the StudioNet script with the two auxiliary wallets.

See [proof obligation](docs/PROOF_OBLIGATION.md),
[threat model](docs/THREAT_MODEL.md), [test matrix](docs/TEST_MATRIX.md), and
[test-resource manifest](docs/TEST_RESOURCE_MANIFEST.md).
