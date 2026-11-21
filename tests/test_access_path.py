import json

import pytest


def test_route_features_bind_each_answer_and_deduplicate(direct_vm, direct_deploy, direct_bob):
    contract = direct_deploy("access_path.py")
    direct_vm.mock_llm("Assess public accessibility", " yes, unknown, no ")
    args = ("Library", "West entrance", "The west entrance is step-free and has no lift.")
    index = contract.assess(*args)
    card = json.loads(contract.get_report(index))
    assert card["features"] == {
        "step_free_entry": "YES",
        "accessible_restroom": "UNKNOWN",
        "lift_serves_route": "NO",
    }
    assert len(card["evidence_sha256"]) == 64
    assert direct_vm.run_validator()
    assert not direct_vm.run_validator(leader_result="YES,YES,NO")

    direct_vm.clear_mocks()
    assert contract.assess(*args) == index
    assert contract.count() == 1

    with direct_vm.prank(direct_bob):
        direct_vm.mock_llm("Assess public accessibility", "NO,UNKNOWN,NO")
        assert contract.assess(*args) != index
    assert contract.count() == 2


def test_malformed_response_is_never_an_access_card(direct_vm, direct_deploy):
    contract = direct_deploy("access_path.py")
    direct_vm.mock_llm("Assess public accessibility", "YES,YES")
    with pytest.raises(Exception, match="invalid access"):
        contract.assess("Library", "West", "Missing details.")
    assert contract.count() == 0
