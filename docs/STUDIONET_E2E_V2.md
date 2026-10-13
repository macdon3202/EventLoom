# EventLoom V2 StudioNet evidence

Contract: [0xF1328d04f45f2aC59dd212c8687897d54288C719](https://explorer-studio.genlayer.com/address/0xF1328d04f45f2aC59dd212c8687897d54288C719)

Configuration readback confirms `EVENT_LOOM_V2`, architecture
`DUAL_ABI_OBLIGATION_COMPATIBILITY_LATTICE`, and `deployer_authority = NONE`.

The main wallet deployed only. Auxiliary A
`0xFeD97e2aE1A8C1983b7cA206B3545e6A2c685E43` creates dossiers; auxiliary B
`0xc67532aeF9D2879cBA9375a02E6217A3524657B8` evaluates them.

## Happy path

- [Create dossier](https://explorer-studio.genlayer.com/tx/0xbbfa6c59c5e7f44b625648a56509750209f42e6599afc5311a8ed6a92e90323a)
- [Evaluate dossier](https://explorer-studio.genlayer.com/tx/0x48bdf9413a15a86d1c129211cdc5b8be7ed3e0baa5f97bb3ed4f12fc73f7f831)

Both finalized `MAJORITY_AGREE / SUCCESS`. Final standing: `COMPATIBLE`.

Sources: verified [WETH9](https://optimism.blockscout.com/api/v2/smart-contracts/0x4200000000000000000000000000000000000006)
and [USDT](https://optimism.blockscout.com/api/v2/smart-contracts/0x94b008aA00579c1307B0EF2c499aD98a8ce58e58).
Obligation: exact non-anonymous `Transfer(address indexed,address indexed,uint256)`.
This is an interface comparison, not a claim that these assets migrated.

Full create/evaluate receipts and sealed/final readbacks:
[studionet-e2e-v2.json](studionet-e2e-v2.json).

## Adversarial audit

Checkpointed live audit: [LIVE_AUDIT_V2.md](LIVE_AUDIT_V2.md).
Full receipts and complete before/after readbacks:
[live-audit-v2.json](live-audit-v2.json).

All 11 audit transactions finalized with majority agreement. Five expected
rejections matched their error codes and preserved the entire recorded contract
state. Together with the two happy-path transactions, this run records 13
finalized transactions on the V2 deployment.

Final dossier states:

| Dossier | Actual result | Interpretation |
|---|---|---|
| 1 | `COMPATIBLE` | Exact verified non-anonymous Transfer interface |
| 2 | `REVIEW_REQUIRED` | New source cannot establish verified ABI |
| 3 | `REVIEW_REQUIRED` | Semantic equivalence remained UNKNOWN |
| 4 | `REVIEW_REQUIRED` | NFT source exceeded the bounded response size |

The last case is source-size rejection, not a committed layout-BREAKING result.

## Coverage boundary

Local tests establish corrected anonymous-event behavior and terminal
`ADAPTER_REQUIRED` rename behavior. Do not present local mocks as real source
observations. No live `BREAKING` or `ADAPTER_REQUIRED` outcome is claimed unless
the corresponding final dossier actually records it. Validator failure and
forced network/model faults remain local coverage unless they occur live.
