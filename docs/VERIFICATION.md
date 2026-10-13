# Verification record

Current V2 source: 33 tests passed; GenVM lint and validation passed.
V1 audit previously reproduced an anonymous-event false positive (29 passed,
1 failed). V2 correction details: [V2_CHANGES.md](V2_CHANGES.md).

Date: 2026-10-13

- `py -3.12 -m pytest tests -q --tb=short -p no:cacheprovider`
- Current V2 result: `33 passed`.
- `PYTHONUTF8=1 genvm-lint check contracts/event_loom.py`
- Result: lint passed (3 checks), validation passed, 5 public methods.
- Runner is pinned to v0.2.16 and an immutable dependency hash.

The one unused-LLM-mock warning is expected: the baseline-invalid branch stops
before semantic mapping. The Windows-only test shim delays deletion of gltest's
temporary stdin file; it does not alter VM, consensus or contract behavior.

Historical V1 StudioNet deployment: `0x1BEd25324D7F520433e84B51777Ee80d0Df9dBf0`.
Live `COMPATIBLE` and unverified-source `REVIEW_REQUIRED` cases finalized with
majority agreement and were confirmed by contract readback. Details and all
transaction links: [STUDIONET_E2E.md](STUDIONET_E2E.md).

V2 deployment: `0xF1328d04f45f2aC59dd212c8687897d54288C719`.
V2 happy path finalized `COMPATIBLE`; unverified source finalized
`REVIEW_REQUIRED`. Live permission, duplicate and terminal-replay checks compare
complete before/after state. Evidence: [STUDIONET_E2E_V2.md](STUDIONET_E2E_V2.md).
V1 receipts remain historical and do not verify V2 code.
