# EventLoom StudioNet E2E

Expanded audit: [LIVE_AUDIT.md](LIVE_AUDIT.md), with full state rollback
comparisons and additional uncertainty/source-size cases. V1 has known safety
findings documented in [AUDIT_FINDINGS.md](AUDIT_FINDINGS.md).

Date: 2026-10-13

Contract: [0x1BEd25324D7F520433e84B51777Ee80d0Df9dBf0](https://explorer-studio.genlayer.com/address/0x1BEd25324D7F520433e84B51777Ee80d0Df9dBf0)

The main wallet deployed only. Auxiliary wallet A created dossiers and auxiliary
wallet B evaluated them. Configuration confirms `EVENT_LOOM_V1` and
`deployer_authority = NONE`. Full receipts, wallet addresses, ABI digests and
final readbacks are in [studionet-e2e.json](studionet-e2e.json).

## Compatible interface

Sources: [WETH9 ABI](https://optimism.blockscout.com/api/v2/smart-contracts/0x4200000000000000000000000000000000000006)
and [USDT ABI](https://optimism.blockscout.com/api/v2/smart-contracts/0x94b008aA00579c1307B0EF2c499aD98a8ce58e58).

This is an interface demonstration; it does not assert a real WETH-to-USDT migration.
Both verified ABIs preserve `Transfer(address indexed,address indexed,uint256)`.

- [Create dossier 1](https://explorer-studio.genlayer.com/tx/0x224a95bb4be4aa5f38e6ef8c9cd89859b6071d1df2f67521855482ba8343a98b)
- [Evaluate dossier 1](https://explorer-studio.genlayer.com/tx/0xee924c4ec6fce55ba3cac1e0deb9ab1b268b39e6e7a64328ba026c7da6279f5c)

Both finalized `MAJORITY_AGREE / SUCCESS`. Final readback: `COMPATIBLE`.

## Unverified source failure

Old source: WETH9. New source:
[0x1111111111111111111111111111111111111111](https://optimism.blockscout.com/api/v2/smart-contracts/0x1111111111111111111111111111111111111111).
The new endpoint cannot establish a verified ABI.

- [Create dossier 2](https://explorer-studio.genlayer.com/tx/0xed7c0979c1347baf88bea0d9b02118290733255fab73fdd1501f2ab4a90ffe20)
- [Evaluate dossier 2](https://explorer-studio.genlayer.com/tx/0x9fbd4edc7e9aee3e3ce1afc2cd5c04fe7253d5b567903ce79a218ecdf92df05f)

Both finalized `MAJORITY_AGREE / SUCCESS`. Final readback: `REVIEW_REQUIRED`.

## Coverage boundary

These live cases establish exact ABI compatibility and source failure handling.
Semantic rename, confirmed `BREAKING`, replay, permission rejection, rollback
and validator conflict are currently local-test coverage, not claimed live.
