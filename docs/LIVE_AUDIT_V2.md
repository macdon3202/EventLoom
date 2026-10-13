# Live adversarial audit V2

Contract: `0xF1328d04f45f2aC59dd212c8687897d54288C719`

| Case | Transaction | Verified result |
|---|---|---|
| create_unverified | [Explorer](https://explorer-studio.genlayer.com/tx/0xe40562e5b4729bb3138aeb365dc6f5fd02ae19855827c5c38afc1e8c99c0a270) | MAJORITY_AGREE |
| evaluate_unverified | [Explorer](https://explorer-studio.genlayer.com/tx/0xe7f7653b6928e66f0276430569232bda171fd53bd5a21f6df8280a31195fb191) | MAJORITY_AGREE; REVIEW_REQUIRED / VERIFIED_ABI_NOT_ESTABLISHED |
| creator_self_evaluation | [Explorer](https://explorer-studio.genlayer.com/tx/0xd3f3955d77f3b63d5b9ebc4bf85a9ebc1fb271d2baf9e219828e66d88f46ea86) | Expected revert; complete state unchanged |
| terminal_replay | [Explorer](https://explorer-studio.genlayer.com/tx/0xdcf6440b22f6f341abfd547635cbf08c6f77a65725510260189c58d46765bedd) | Expected revert; complete state unchanged |
| unauthorized_cancel | [Explorer](https://explorer-studio.genlayer.com/tx/0xdbdd6db6f906d41214b0afbcc6b1cad676b3597c49a57453e1f00308f7e2c906) | Expected revert; complete state unchanged |
| duplicate_dossier | [Explorer](https://explorer-studio.genlayer.com/tx/0x56a1fc158d409e943e0e0eec6d4f01b08090cd52e5806709c8c2619af50aff22) | Expected revert; complete state unchanged |
| create_breaking | [Explorer](https://explorer-studio.genlayer.com/tx/0xc9cfc73a178ab4e62716b6d41b5501194a550e13f9c8a10d8d9dffaf6f8ef71e) | MAJORITY_AGREE |
| sealed_self_evaluation | [Explorer](https://explorer-studio.genlayer.com/tx/0x981bf6eaa6c5c4581eedc66b56358994bc5158876d6ee205bcf468901c448cd9) | Expected revert; complete state unchanged |
| evaluate_breaking | [Explorer](https://explorer-studio.genlayer.com/tx/0x3e5464c501e30e33bb4a8bf64c7ae3006b6c1191b519bc43718541ab0a384201) | MAJORITY_AGREE; REVIEW_REQUIRED / SEMANTIC_EQUIVALENCE_UNKNOWN |
| create_indexed_breaking | [Explorer](https://explorer-studio.genlayer.com/tx/0x9d967ae31024fd1de953d9499395bdc38515a9fc0ec7ca765723fe34455b48bb) | MAJORITY_AGREE |
| evaluate_indexed_breaking | [Explorer](https://explorer-studio.genlayer.com/tx/0xb2eb6fa2601144b00efd6830d3b68d97cb38a2a79346a8094aaf29d849fa0122) | MAJORITY_AGREE; REVIEW_REQUIRED / VERIFIED_ABI_NOT_ESTABLISHED |

Full before/after snapshots and receipts: [live-audit-v2.json](live-audit-v2.json).

V1 safety findings and V2 correction history: [AUDIT_FINDINGS.md](AUDIT_FINDINGS.md).
