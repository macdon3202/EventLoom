# Test matrix

| Path / adversarial case | Required result | Covered locally |
|---|---|---|
| Exact event and exact layout preserved | `COMPATIBLE` | Yes |
| Clear semantic rename with exact layout | `ADAPTER_REQUIRED` | Yes |
| New same-name event becomes anonymous | `BREAKING` | Yes |
| Anonymous baseline | `REVIEW_REQUIRED` | Yes |
| AI maps to anonymous renamed event | `REVIEW_REQUIRED` | Yes |
| Adapter-required standing replay | Revert + unchanged | Yes |
| Same name but changed `indexed` layout | `BREAKING` | Yes |
| Missing event with definite semantic `NO` | `BREAKING` | Yes |
| Semantic `UNKNOWN` | `REVIEW_REQUIRED` | Yes |
| AI maps nonexistent event | `REVIEW_REQUIRED` | Yes |
| Malformed AI response | `REVIEW_REQUIRED` | Yes |
| Baseline obligation absent | `REVIEW_REQUIRED` | Yes |
| Old/new ABI unverified | `REVIEW_REQUIRED` | Yes |
| ABI missing/malformed | `REVIEW_REQUIRED` | Yes |
| Source 5xx | `RETRYABLE`; no partial digest | Yes |
| Creator self-evaluation | Revert + complete rollback | Yes |
| Terminal replay | Revert + complete rollback | Yes |
| Duplicate pair + obligations | Revert + counter unchanged | Yes |
| Prompt injection | No positive bypass | Yes |
| Consensus failure | Non-positive | Yes |
| Invalid input | Revert + no dossier | Yes |
| Arbitrary non-deployer creator | Success | Yes |
| Deployer authority | Exactly `NONE` | Yes |

V2 local result on 2026-10-13: 33 passed. V2 StudioNet rows remain pending until a
deployment address is supplied and every live transaction has finalized with
post-write readback.
