"""Checkpoint every live audit write and compare full state on rejection."""
import json
import os
import time
import sys
from run_studionet_e2e import ROOT, RPC, EXPLORER, load_wallets, read, plain
from genlayer_py import create_account, create_client
from genlayer_py.chains import studionet

ADDRESS = sys.argv[1] if len(sys.argv) > 1 else "0x1BEd25324D7F520433e84B51777Ee80d0Df9dBf0"
TARGET = ROOT / "docs" / ("live-audit-v2.json" if len(sys.argv) > 1 else "live-audit.json")

def main():
    load_wallets()
    a = create_account(os.environ["SERVICE_LEDGER_KEY_A"])
    b = create_account(os.environ["SERVICE_LEDGER_KEY_B"])
    c = create_client(chain=studionet, account=a, endpoint=RPC)
    config = read(c, ADDRESS, a, "get_config", [])
    if len(sys.argv) > 1:
        assert config["version"] == "EVENT_LOOM_V2" and config["deployer_authority"] == "NONE"
    evidence = json.loads(TARGET.read_text()) if TARGET.exists() else {}
    def save(): TARGET.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    def snapshot():
        config = read(c, ADDRESS, a, "get_config", [])
        return {"config": config, "dossiers": [read(c, ADDRESS, a, "get_dossier", [i]) for i in range(1, config["dossier_count"] + 1)]}
    def case(label, actor, method, args, rejection=None):
        item = evidence.setdefault(label, {})
        if item.get("complete"): return
        if "hash" not in item:
            item["before"] = snapshot()
            item["hash"] = str(c.write_contract(address=ADDRESS, function_name=method, account=actor, args=args, value=0))
            item["url"] = EXPLORER + "/tx/" + item["hash"]
            save()
            print(label, item["hash"], flush=True)
        for _ in range(200):
            try: info = plain(c.get_transaction(item["hash"]))
            except Exception: time.sleep(3); continue
            if info.get("status_name") == "FINALIZED": break
            time.sleep(3)
        else: raise TimeoutError(item["hash"])
        receipts = info.get("consensus_data", {}).get("leader_receipt", [])
        if isinstance(receipts, dict): receipts = [receipts]
        item["status"] = info.get("status_name")
        item["consensus"] = info.get("result_name")
        item["receipts"] = [{k:r.get(k) for k in ("mode", "execution_result", "result", "genvm_result")} for r in receipts]
        item["after"] = snapshot()
        if rejection:
            item["rollback_equal"] = item["before"] == item["after"]
            item["expected_error"] = rejection
            item["error_found"] = rejection in json.dumps(item["receipts"])
            save()
            assert item["rollback_equal"] and item["error_found"], label
        item["complete"] = True
        save()
        print(label, item["consensus"], "complete", flush=True)
    first = read(c, ADDRESS, a, "get_dossier", [1])
    if len(sys.argv) > 1:
        case("create_unverified", a, "create_dossier", ["OPTIMISM", first["old_contract"], "0x1111111111111111111111111111111111111111", "v2-unverified-source", first["obligations"]])
        source_id = evidence["create_unverified"]["after"]["config"]["dossier_count"]
        case("evaluate_unverified", b, "evaluate_compatibility", [source_id])
        assert evidence["evaluate_unverified"]["after"]["dossiers"][source_id - 1]["state"] == "REVIEW_REQUIRED"
    case("creator_self_evaluation", a, "evaluate_compatibility", [1], "DOSSIER_NOT_EVALUABLE")
    case("terminal_replay", b, "evaluate_compatibility", [1], "DOSSIER_NOT_EVALUABLE")
    case("unauthorized_cancel", b, "cancel_dossier", [2], "CREATOR_REQUIRED")
    case("duplicate_dossier", a, "create_dossier", [first["chain_key"], first["old_contract"], first["new_contract"], first["migration_ref"], first["obligations"]], "DOSSIER_ALREADY_EXISTS")
    obligation = json.dumps([{"event":"Deposit", "inputs":[{"type":"address","indexed":True},{"type":"uint256","indexed":False}], "semantic_purpose":"Notify indexers of native currency deposited to mint wrapped native tokens."}], separators=(",", ":"))
    case("create_breaking", a, "create_dossier", ["OPTIMISM", first["old_contract"], first["new_contract"], "audit-missing-wrapped-native-deposit", obligation])
    count = evidence["create_breaking"]["after"]["config"]["dossier_count"]
    case("sealed_self_evaluation", a, "evaluate_compatibility", [count], "INDEPENDENT_EVALUATOR_REQUIRED")
    case("evaluate_breaking", b, "evaluate_compatibility", [count])
    case("create_indexed_breaking", a, "create_dossier", ["OPTIMISM", first["old_contract"], "0xC36442b4a4522E871399CD717aBDD847Ab11FE88", "audit-erc20-to-erc721-indexed-layout", first["obligations"]])
    indexed_id = evidence["create_indexed_breaking"]["after"]["config"]["dossier_count"]
    case("evaluate_indexed_breaking", b, "evaluate_compatibility", [indexed_id])
    if len(sys.argv) == 1:
        assert evidence["evaluate_indexed_breaking"]["after"]["dossiers"][indexed_id - 1]["state"] == "BREAKING"

if __name__ == "__main__": main()
