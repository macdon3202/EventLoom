"""Render checkpointed receipts without claiming unfinished cases passed."""
import json
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
v2 = len(sys.argv) > 1 and sys.argv[1] == "v2"
filename = "live-audit-v2.json" if v2 else "live-audit.json"
data = json.loads((root / "docs" / filename).read_text())
address = "0xF1328d04f45f2aC59dd212c8687897d54288C719" if v2 else "0x1BEd25324D7F520433e84B51777Ee80d0Df9dBf0"
lines = ["# Live adversarial audit" + (" V2" if v2 else " V1"), "", "Contract: `" + address + "`", "", "| Case | Transaction | Verified result |", "|---|---|---|"]
for label, case in data.items():
    tx = "[Explorer](" + case["url"] + ")" if case.get("url") else "Not submitted"
    if case.get("complete"):
        outcome = "Expected revert; complete state unchanged" if case.get("rollback_equal") else case.get("consensus", "Complete")
        if label.startswith("evaluate_") and case.get("after"):
            newest = case["after"]["dossiers"][-1]
            outcome += "; " + newest["state"] + " / " + newest["reason"]
    else:
        outcome = "Pending / not yet verified"
    lines.append("| " + label + " | " + tx + " | " + outcome + " |")
lines += ["", "Full before/after snapshots and receipts: [" + filename + "](" + filename + ").", "", "V1 safety findings and V2 correction history: [AUDIT_FINDINGS.md](AUDIT_FINDINGS.md)."]
(root / "docs" / ("LIVE_AUDIT_V2.md" if v2 else "LIVE_AUDIT.md")).write_text("\n".join(lines) + "\n", encoding="utf-8")
