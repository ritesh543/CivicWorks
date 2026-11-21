import json

import pytest


def test_only_publisher_can_activate_a_matching_mapping(direct_deploy, direct_vm, direct_bob):
    contract = direct_deploy("open_field_map.py")
    direct_vm.mock_llm("Compare an open-data column", "MATCH")
    first = contract.propose("paths@1", "path_cm", "Unobstructed walkway width", "cm", "PATH_WIDTH")
    assert json.loads(contract.get_proposal(first))["target_unit"] == "mm"
    assert not direct_vm.run_validator(leader_result="DIFFERENT")
    with pytest.raises(Exception, match="inactive"):
        contract.normalize(first, 140)
    with direct_vm.prank(direct_bob), pytest.raises(Exception, match="only the proposal publisher"):
        contract.activate(first)
    contract.activate(first)
    assert contract.normalize(first, 140) == 1400
    second = contract.propose("paths@1", "path_cm", "Walkway width", "mm", "PATH_WIDTH")
    with pytest.raises(Exception, match="already mapped"):
        contract.activate(second)
    assert contract.normalize(first, 140) == 1400


def test_dimension_and_unresolved_evidence_are_separate_gates(direct_deploy, direct_vm):
    contract = direct_deploy("open_field_map.py")
    with pytest.raises(Exception, match="incompatible unit"):
        contract.propose("rev", "col", "Some duration", "l", "CLOSURE_DURATION")
    assert contract.count() == 0
    direct_vm.mock_llm("Compare an open-data column", "UNCLEAR")
    index = contract.propose("rev", "col", "Unspecified length", "m", "DOOR_CLEARANCE")
    with pytest.raises(Exception, match="no matching review"):
        contract.activate(index)
