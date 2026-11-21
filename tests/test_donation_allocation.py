import json

import pytest


def test_reservations_are_organizer_only_and_conserve_capacity(direct_deploy, direct_vm, direct_bob):
    contract = direct_deploy("donation_allocation.py")
    channel = contract.open_channel("School reuse", "Only intact chairs with all feet attached.", 10)
    direct_vm.mock_llm("Compare a donated lot", "ELIGIBLE")
    with direct_vm.prank(direct_bob):
        first = contract.submit_lot(channel, "A", 8, "All chairs are intact with all feet.")
        second = contract.submit_lot(channel, "B", 6, "All chairs are intact with all feet.")
        with pytest.raises(Exception, match="only the channel organizer"):
            contract.reserve(first)
    assert not direct_vm.run_validator(leader_result="UNCLEAR")
    contract.reserve(first)
    with pytest.raises(Exception, match="insufficient channel capacity"):
        contract.reserve(second)
    contract.complete(first, False)
    contract.reserve(second)
    contract.complete(second, True)
    state = json.loads(contract.get_channel(channel))
    assert (state["remaining"], state["reserved"], state["distributed"]) == (4, 0, 6)
    with pytest.raises(Exception, match="no active reservation"):
        contract.complete(second, False)


def test_unclear_lot_cannot_debit_capacity(direct_deploy, direct_vm):
    contract = direct_deploy("donation_allocation.py")
    channel = contract.open_channel("Community reuse", "Clean and tested fans", 5)
    direct_vm.mock_llm("Compare a donated lot", "UNCLEAR")
    item = contract.submit_lot(channel, "F", 1, "A fan was collected.")
    with pytest.raises(Exception, match="did not meet"):
        contract.reserve(item)
    assert json.loads(contract.get_channel(channel))["remaining"] == 5
