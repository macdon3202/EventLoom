"""Run EventLoom fixtures with two auxiliary, non-deployer wallets."""
from __future__ import annotations
import json
import os
from pathlib import Path
import sys
import time
from genlayer_py import create_account, create_client
from genlayer_py.chains import studionet

RPC = "https://studio.genlayer.com/api"
EXPLORER = "https://explorer-studio.genlayer.com"
ROOT = Path(__file__).resolve().parents[1]


def load_wallets():
    path = ROOT.parent / "secrets" / "genlayer-test-wallets.env"
    for raw in path.read_text(encoding="utf-8").splitlines():
        if "=" in raw and not raw.lstrip().startswith("#"):
            key, value = raw.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip("'\"").strip("<>"))


def plain(value):
    if isinstance(value, dict): return {str(k): plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)): return [plain(v) for v in value]
    return value if isinstance(value, (str, int, float, bool)) or value is None else str(value)


def tx_signals(info):
    status = str(info.get("status_name") or info.get("statusName") or info.get("status") or "UNKNOWN").upper()
    consensus = str(info.get("result_name") or info.get("consensus_result_name") or info.get("consensus_result") or "UNKNOWN").upper()
    data = info.get("consensus_data") if isinstance(info.get("consensus_data"), dict) else {}
    receipts = data.get("leader_receipt") or data.get("validators") or []
    if isinstance(receipts, dict): receipts = [receipts]
    successful = next((r for r in receipts if isinstance(r, dict) and (r.get("execution_result") == "SUCCESS" or r.get("genvm_result", {}).get("execution_result") == "SUCCESS")), {})
    result = successful.get("result") if isinstance(successful.get("result"), dict) else {}
    payload = result.get("payload") if isinstance(result.get("payload"), dict) else {}
    execution = str(successful.get("execution_result") or successful.get("genvm_result", {}).get("execution_result") or info.get("execution_result") or "UNKNOWN").upper()
    return status, consensus, execution, payload.get("readable") or result.get("readable")


def wait(client, tx_hash):
    for _ in range(200):
        try:
            info = plain(client.get_transaction(tx_hash))
        except Exception as exc:
            print(json.dumps({"poll_retry": tx_hash, "error": type(exc).__name__}), flush=True)
            time.sleep(3); continue
        status, consensus, execution, returned = tx_signals(info)
        if status == "FINALIZED":
            if consensus not in {"MAJORITY_AGREE", "AGREE", "ACCEPTED"} or execution != "SUCCESS":
                raise AssertionError({"tx": tx_hash, "status": status, "consensus": consensus, "execution": execution})
            return {"hash": tx_hash, "url": f"{EXPLORER}/tx/{tx_hash}", "status": status, "consensus": consensus, "execution": execution, "returned": returned}
        time.sleep(3)
    raise TimeoutError(tx_hash)


def write(client, address, account, method, args):
    tx_hash = str(client.write_contract(address=address, function_name=method, account=account, args=args, value=0))
    print(json.dumps({"submitted": tx_hash, "method": method}), flush=True)
    return wait(client, tx_hash)


def read(client, address, account, method, args):
    for attempt in range(8):
        try:
            return plain(client.read_contract(address=address, function_name=method, args=args, account=account))
        except Exception:
            if attempt == 7: raise
            time.sleep(3)


def main():
    if len(sys.argv) != 3: raise SystemExit("usage: run_studionet_e2e.py CONTRACT_ADDRESS FIXTURES_JSON")
    contract, fixture_path = sys.argv[1], Path(sys.argv[2])
    fixtures = json.loads(fixture_path.read_text(encoding="utf-8"))
    if not isinstance(fixtures, list) or not fixtures: raise ValueError("FIXTURES_MUST_BE_NONEMPTY_LIST")
    load_wallets()
    wallet_a = create_account(os.environ["SERVICE_LEDGER_KEY_A"])
    wallet_b = create_account(os.environ["SERVICE_LEDGER_KEY_B"])
    client = create_client(chain=studionet, account=wallet_a, endpoint=RPC)
    config = read(client, contract, wallet_a, "get_config", [])
    if config.get("version") != "EVENT_LOOM_V2" or config.get("deployer_authority") != "NONE": raise AssertionError(config)
    roots = {"OPTIMISM": "https://optimism.blockscout.com/api/v2/smart-contracts/", "BASE": "https://base.blockscout.com/api/v2/smart-contracts/"}
    required = {"chain_key", "old_contract", "new_contract", "migration_ref", "event_obligations", "expected_state", "old_source_url", "new_source_url"}
    cases = []
    for fixture in fixtures:
        if not isinstance(fixture, dict) or set(fixture) != required: raise ValueError("INVALID_FIXTURE_SCHEMA")
        root = roots[fixture["chain_key"]]
        if fixture["old_source_url"].lower() != root + fixture["old_contract"].lower(): raise ValueError("OLD_SOURCE_URL_NOT_CANONICAL")
        if fixture["new_source_url"].lower() != root + fixture["new_contract"].lower(): raise ValueError("NEW_SOURCE_URL_NOT_CANONICAL")
        opened = write(client, contract, wallet_a, "create_dossier", [fixture["chain_key"], fixture["old_contract"], fixture["new_contract"], fixture["migration_ref"], fixture["event_obligations"]])
        dossier_id = int(str(opened["returned"]).strip('"'))
        sealed = read(client, contract, wallet_a, "get_dossier", [dossier_id])
        evaluated = write(client, contract, wallet_b, "evaluate_compatibility", [dossier_id])
        final = read(client, contract, wallet_b, "get_dossier", [dossier_id])
        if sealed["state"] != "SEALED" or final["state"] != fixture["expected_state"]: raise AssertionError({"fixture": fixture, "sealed": sealed, "final": final})
        cases.append({"fixture": fixture, "dossier_id": dossier_id, "create": opened, "sealed_readback": sealed, "evaluate": evaluated, "final_readback": final})
    evidence = {"network": "studionet", "contract": contract, "contract_url": f"{EXPLORER}/address/{contract}", "wallet_a_creator": str(wallet_a.address), "wallet_b_evaluator": str(wallet_b.address), "main_wallet_used_in_lifecycle": False, "config": config, "cases": cases}
    (ROOT / "docs" / "studionet-e2e-v2.json").write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(evidence, indent=2))


if __name__ == "__main__": main()
