import json

import pytest


def test_rollover_requires_evidence_and_feasible_arithmetic(direct_deploy, direct_vm):
    contract = direct_deploy("meter_continuity.py")
    meter = contract.register("PUMP-3", 1000, 60, 990, 10)
    missed = contract.observe(meter, 5, 20, "")
    assert json.loads(contract.get_reading(missed))["status"] == "HELD_BACKWARD_READING"
    assert json.loads(contract.get_meter(meter))["last_display"] == 990

    direct_vm.mock_llm("Classify a public maintenance note", "ROLLOVER")
    event = contract.observe(meter, 5, 20, "Same meter PUMP-3 wrapped at reading 999.")
    assert json.loads(contract.get_reading(event))["credited_increment"] == 15
    assert not direct_vm.run_validator(leader_result="REPLACEMENT")
    huge = contract.observe(meter, 3, 30, "Same meter wrapped again.")
    assert json.loads(contract.get_reading(huge))["status"] == "HELD_BACKWARD_READING"
    assert json.loads(contract.get_meter(meter))["cumulative_increment"] == 15


def test_replacement_begins_a_new_segment_without_fake_usage(direct_deploy, direct_vm, direct_bob):
    contract = direct_deploy("meter_continuity.py")
    meter = contract.register("PUMP-3", 1000, 40, 400, 10)
    contract.observe(meter, 420, 20, "")
    with direct_vm.prank(direct_bob), pytest.raises(Exception, match="only the meter operator"):
        contract.observe(meter, 1, 30, "New meter.")
    direct_vm.mock_llm("Classify a public maintenance note", "REPLACEMENT")
    contract.observe(meter, 1, 30, "Old instrument was removed and a new one installed.")
    state = json.loads(contract.get_meter(meter))
    assert state["segment"] == 2 and state["cumulative_increment"] == 20
    assert state["last_display"] == 1
    with pytest.raises(Exception, match="follow the accepted baseline"):
        contract.observe(meter, 2, 30, "")
