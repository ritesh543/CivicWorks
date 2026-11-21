import json

import pytest


def test_condition_change_requires_sender_resolution(direct_deploy, direct_vm, direct_bob, direct_charlie):
    contract = direct_deploy("handoff_condition.py")
    index = contract.offer("PA-16", "0x" + direct_bob.hex(), "Powered speaker works and has no cabinet damage.")
    with pytest.raises(Exception, match="open handoff"):
        contract.offer("PA-16", "0x" + direct_charlie.hex(), "Another offer.")
    with pytest.raises(Exception, match="named recipient"):
        contract.inspect(index, "Works.")
    direct_vm.mock_llm("Compare the declared and observed", "CHANGED")
    with direct_vm.prank(direct_bob):
        assert contract.inspect(index, "Speaker works but the cabinet is cracked.") == "EXCEPTION_REVIEW"
        with pytest.raises(Exception, match="only the offer sender"):
            contract.resolve_exception(index, True, "Accept damage.")
    assert not direct_vm.run_validator(leader_result="MATCH")
    assert contract.resolve_exception(index, True, "Crack recorded for repair.") == "ACCEPTED_WITH_EXCEPTION"
    assert json.loads(contract.get_handoff(index))["assessment"] == "CHANGED"
    assert contract.offer("PA-16", "0x" + direct_charlie.hex(), "Cabinet cracked.") > index


def test_matching_condition_closes_the_offer(direct_deploy, direct_vm, direct_bob):
    contract = direct_deploy("handoff_condition.py")
    index = contract.offer("CART-8", "0x" + direct_bob.hex(), "All wheels roll.")
    direct_vm.mock_llm("Compare the declared and observed", "MATCH")
    with direct_vm.prank(direct_bob):
        assert contract.inspect(index, "Every wheel turns freely.") == "ACCEPTED"
    with pytest.raises(Exception, match="inspected or closed"):
        contract.cancel_offer(index)
