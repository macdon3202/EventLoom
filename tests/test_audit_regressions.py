"""Security audit regressions; assertions express required safety behavior."""
import pytest
from test_event_loom import deploy, create, mock_sources, response, event, TRANSFER, evaluate, CREATOR


def test_anonymous_event_must_not_pass_topic_compatible(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy)
    create(c, direct_vm)
    mock_sources(direct_vm, new=response([event("Transfer", TRANSFER, anonymous=True)]))
    assert evaluate(c, direct_vm) == "BREAKING"


def test_anonymous_baseline_is_not_established(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy); create(c, direct_vm)
    mock_sources(direct_vm, old=response([event("Transfer", TRANSFER, anonymous=True)]))
    assert evaluate(c, direct_vm) == "REVIEW_REQUIRED"
    assert c.get_dossier(1)["reason"] == "BASELINE_OBLIGATION_NOT_FOUND"


def test_semantic_mapping_cannot_bypass_anonymous_mode(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy); create(c, direct_vm)
    mock_sources(direct_vm, new=response([event("ValueMoved", TRANSFER, anonymous=True)]))
    direct_vm.mock_llm("EVENT_LOOM_SEMANTIC_EVENT_V1", [{"equivalent":"YES", "mapped_event":"ValueMoved"}])
    assert evaluate(c, direct_vm) == "REVIEW_REQUIRED"


def test_adapter_required_is_terminal_and_not_compatible(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy); create(c, direct_vm)
    mock_sources(direct_vm, new=response([event("ValueMoved", TRANSFER)]))
    direct_vm.mock_llm("EVENT_LOOM_SEMANTIC_EVENT_V1", [{"equivalent":"YES", "mapped_event":"ValueMoved"}])
    assert evaluate(c, direct_vm) == "ADAPTER_REQUIRED"
    before = c.get_dossier(1)
    with direct_vm.expect_revert("DOSSIER_NOT_EVALUABLE"):
        c.evaluate_compatibility(1)
    assert c.get_dossier(1) == before


@pytest.mark.parametrize("fields", [
    [("address", True), ("uint256", True), ("address", False)],
    [("address", True), ("address", True), ("uint128", False)],
])
def test_parameter_order_and_type_break_compatibility(direct_vm, direct_deploy, fields):
    c = deploy(direct_vm, direct_deploy); create(c, direct_vm)
    mock_sources(direct_vm, new=response([event("Transfer", fields)]))
    assert evaluate(c, direct_vm) == "BREAKING"


def test_source_retry_recovers_with_two_verified_snapshots(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy); create(c, direct_vm)
    mock_sources(direct_vm, old_status=503)
    assert evaluate(c, direct_vm) == "RETRYABLE"
    direct_vm.clear_mocks()
    mock_sources(direct_vm)
    assert evaluate(c, direct_vm) == "COMPATIBLE"
    assert c.get_dossier(1)["evaluation_round"] == 2


def test_cancelled_dossier_is_terminal(direct_vm, direct_deploy):
    c = deploy(direct_vm, direct_deploy); create(c, direct_vm)
    with direct_vm.prank(CREATOR): c.cancel_dossier(1)
    before = c.get_dossier(1)
    with direct_vm.expect_revert("DOSSIER_NOT_EVALUABLE"):
        c.evaluate_compatibility(1)
    assert c.get_dossier(1) == before
