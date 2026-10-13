# Threat model

| Threat | Response |
|---|---|
| User supplies arbitrary source URL | Impossible; only chain key and address are accepted |
| Creator evaluates own dossier | Revert with complete rollback |
| ABI unverified or malformed | `REVIEW_REQUIRED`; never positive |
| 429/5xx/network failure | `RETRYABLE`; no partial snapshot committed |
| Baseline lacks a required event | `REVIEW_REQUIRED`, not compatibility |
| Same-name event changes type/order/indexing | Deterministic `BREAKING` |
| Same-name event becomes anonymous | Deterministic `BREAKING` |
| Anonymous baseline | `REVIEW_REQUIRED` |
| Clear semantic rename | `ADAPTER_REQUIRED`; no existing-indexer compatibility claim |
| Renamed event has incompatible layout | Cannot become semantic-compatible |
| AI returns missing/malformed fields | `REVIEW_REQUIRED` |
| AI maps a nonexistent event | `REVIEW_REQUIRED` |
| Prompt injection in semantic purpose | Treated as delimited data; deterministic gate remains authoritative |
| Validator disagreement | Non-positive retryable standing |
| Duplicate address-pair obligations | Revert before counter mutation |
| Re-evaluate terminal dossier | Revert; record unchanged |
| Deployer intervention | No stored role or privileged method exists |

## Residual limitations

- Verified source metadata may still describe flawed code.
- Proxy endpoints may expose proxy ABI rather than every implementation event.
- ABI compatibility does not imply runtime behavioral compatibility.
- Semantic rename assessment can remain uncertain; uncertainty is deliberately
  non-positive.
