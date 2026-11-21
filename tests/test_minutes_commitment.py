import json

import pytest


def test_validator_checks_the_selected_paragraph_against_full_claim(direct_deploy, direct_vm, direct_bob):
    contract = direct_deploy("minutes_commitment.py")
    adopted = "Resolved: Facilities will replace the lobby bench by Dec 12."
    index = contract.publish("board-17", "Proposal to repaint the lobby by Dec 12.\n" + adopted)
    args = (index, "Replace the lobby bench", "Facilities", "Dec 12")
    with direct_vm.prank(direct_bob), pytest.raises(Exception, match="only the minutes publisher"):
        contract.certify(*args)
    direct_vm.mock_llm("Return only P followed", "P2")
    direct_vm.mock_llm("Does paragraph 2 itself", "APPROVES")
    direct_vm.mock_llm("Does paragraph 1 itself", "REJECTS")
    cert = json.loads(contract.get_certification(contract.certify(*args)))
    assert cert["approved"] is True
    assert cert["paragraph_number"] == 2
    assert cert["source_quote"] == adopted
    assert direct_vm.run_validator()
    assert not direct_vm.run_validator(leader_result=1)
    assert not direct_vm.run_validator(leader_result=0)
    assert not direct_vm.run_validator(leader_result=True)
    direct_vm.clear_mocks()
    assert contract.certify(*args) == 0


def test_deferred_vote_stays_unapproved(direct_deploy, direct_vm):
    contract = direct_deploy("minutes_commitment.py")
    index = contract.publish("board-18", "The committee deferred the vote on the garden path.")
    direct_vm.mock_llm("Return only P followed", "NONE")
    item = json.loads(contract.get_certification(contract.certify(index, "Build path", "Parks", "Dec 1")))
    assert item["approved"] is False
    assert item["source_quote"] == ""
    assert direct_vm.run_validator()
