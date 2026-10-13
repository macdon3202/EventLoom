"""Collect finalized receipts and current on-chain readbacks without writes."""
import json
import os
from run_studionet_e2e import ROOT, RPC, EXPLORER, load_wallets, read, wait
from genlayer_py import create_account, create_client
from genlayer_py.chains import studionet

ADDRESS = "0x1BEd25324D7F520433e84B51777Ee80d0Df9dBf0"
HASHES = [
    "0x224a95bb4be4aa5f38e6ef8c9cd89859b6071d1df2f67521855482ba8343a98b",
    "0xee924c4ec6fce55ba3cac1e0deb9ab1b268b39e6e7a64328ba026c7da6279f5c",
    "0xed7c0979c1347baf88bea0d9b02118290733255fab73fdd1501f2ab4a90ffe20",
    "0x9fbd4edc7e9aee3e3ce1afc2cd5c04fe7253d5b567903ce79a218ecdf92df05f",
]

def main():
    load_wallets()
    a = create_account(os.environ["SERVICE_LEDGER_KEY_A"])
    b = create_account(os.environ["SERVICE_LEDGER_KEY_B"])
    client = create_client(chain=studionet, account=a, endpoint=RPC)
    evidence = {
        "contract": ADDRESS, "contract_url": EXPLORER + "/address/" + ADDRESS,
        "wallet_a": str(a.address), "wallet_b": str(b.address),
        "receipts": [wait(client, h) for h in HASHES],
        "config": read(client, ADDRESS, a, "get_config", []),
        "dossiers": [read(client, ADDRESS, a, "get_dossier", [i]) for i in (1, 2)],
    }
    assert evidence["dossiers"][0]["state"] == "COMPATIBLE"
    assert evidence["dossiers"][1]["state"] == "REVIEW_REQUIRED"
    (ROOT / "docs" / "studionet-e2e.json").write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"states": [d["state"] for d in evidence["dossiers"]], "saved": True}))

if __name__ == "__main__": main()
