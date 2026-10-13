# EventLoom V2 correction record

Date: 2026-10-13

## Anonymous events

V1 compared names and input layouts without enforcing anonymous mode. V2 only
establishes a non-anonymous baseline. Every exact or semantic candidate must
also be non-anonymous. Same-name anonymous replacements cannot pass the positive
gate. Normalization deduplication now includes anonymous mode so entries cannot
silently hide mode differences.

## Semantic renames

V1 treated a semantically similar rename as compatible with an existing indexer.
V2 uses `ADAPTER_REQUIRED` and reason
`EVENT_RENAME_REQUIRES_INDEXER_ADAPTER`. This is a terminal advisory result;
it never proves an indexer adapter exists or works. Only exact event preservation
can return `COMPATIBLE`.

## Retry response validation

When either source is unavailable, both snapshot digests remain empty. The
response validator now explicitly accepts this retry shape even when the other
source succeeded, preserving the source statuses rather than replacing them with
generic failure metadata.

## Verification

- 33 tests passed, including all three anonymous-mode branches, rename standing,
  terminal replay and retry recovery.
- GenVM lint passed (3 checks) and contract validation passed (5 public methods).
- V2 source: `contracts/event_loom.py`, version `EVENT_LOOM_V2`.
- V2 deployed at `0xF1328d04f45f2aC59dd212c8687897d54288C719`;
  actual live outcomes are documented in `STUDIONET_E2E_V2.md`.
- Existing address `0x1BEd25324D7F520433e84B51777Ee80d0Df9dBf0` remains V1.
- Deploy V2 with the main wallet and no constructor arguments, then use auxiliary
  wallets for fresh evidence. The runner rejects V1 and writes its V2 output to
  `docs/studionet-e2e-v2.json` to preserve historical V1 evidence.

The original 220,000-byte source-response bound remains explicit. Oversized
sources are rejected; no live BREAKING or semantic-rename outcome is claimed
for V2 before deployment.
