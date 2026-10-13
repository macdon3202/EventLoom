# Live adversarial audit

Contract: `0x1BEd25324D7F520433e84B51777Ee80d0Df9dBf0`

| Case | Transaction | Verified result |
|---|---|---|
| creator_self_evaluation | [Explorer](https://explorer-studio.genlayer.com/tx/0xe115b4701e0f4fecb9f364b1ffbcb81e9de5ac1fbac83e5ed1f02c8b5a8a1228) | Expected revert; complete state unchanged |
| terminal_replay | [Explorer](https://explorer-studio.genlayer.com/tx/0x4b891c7075c0e2f10cdde19bead934fca648519a1e203836f42283c615ffc238) | Expected revert; complete state unchanged |
| unauthorized_cancel | [Explorer](https://explorer-studio.genlayer.com/tx/0xf5a7dbb46c4b7e18e88bda8725b642df736487b4a3ec9e7b474f932d4a824f16) | Expected revert; complete state unchanged |
| duplicate_dossier | [Explorer](https://explorer-studio.genlayer.com/tx/0xf3b13e3991b61e4e7379b87857cae566c7fbeb4b77566b401679f696eb593645) | Expected revert; complete state unchanged |
| create_breaking | [Explorer](https://explorer-studio.genlayer.com/tx/0xcc510ee4de4c585cd00fd39a488350e8fb8ea5fcec108bf6e60ed81e0da50441) | MAJORITY_AGREE |
| sealed_self_evaluation | [Explorer](https://explorer-studio.genlayer.com/tx/0x9dfa51f0c547f5ef97ade313067ccf258104e2c4c946de6bec7d09c7ec850d76) | Expected revert; complete state unchanged |
| evaluate_breaking | [Explorer](https://explorer-studio.genlayer.com/tx/0x063e4a3182cc066175f46da7f6862015f8445cbcfc72e57458c287e4722c69cc) | MAJORITY_AGREE; REVIEW_REQUIRED / SEMANTIC_EQUIVALENCE_UNKNOWN |
| create_indexed_breaking | [Explorer](https://explorer-studio.genlayer.com/tx/0x8d624db2bcb50490141a6f5e6ab8bf0c22ccc714cd92c1d15a1944a3f2f18453) | MAJORITY_AGREE |
| evaluate_indexed_breaking | [Explorer](https://explorer-studio.genlayer.com/tx/0xfc1f12fd6cc87223520cfa8bfd62e25cd087b98df79574a2c577bf731943b679) | MAJORITY_AGREE; REVIEW_REQUIRED / VERIFIED_ABI_NOT_ESTABLISHED |

Full before/after snapshots and receipts: [live-audit.json](live-audit.json).

Known V1 safety findings: [AUDIT_FINDINGS.md](AUDIT_FINDINGS.md).
