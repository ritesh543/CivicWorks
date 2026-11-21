import json

import pytest


def test_a_confirmed_link_keeps_the_primary_at_one_level(direct_vm, direct_deploy):
    contract = direct_deploy("repair_merge.py")
    root = contract.file_report("SITE-1", 600, "Door D2 closer jams.")
    previous_root = contract.file_report("SITE-1", 610, "D2 closer sticks midway.")
    child = contract.file_report("site-1", 620, "Door D2 closer sticks before closing.")
    direct_vm.mock_llm("untrusted facilities work-order", "SAME_FAULT")
    assert contract.review_duplicate(child, previous_root) == "SAME_FAULT"
    assert json.loads(contract.get_report(child))["duplicate_of"] == previous_root
    assert json.loads(contract.get_report(previous_root))["linked_reports"] == 1
    assert direct_vm.run_validator()
    assert not direct_vm.run_validator(leader_result="DIFFERENT")
    with pytest.raises(Exception, match="already serves as a primary"):
        contract.review_duplicate(previous_root, root)
    with pytest.raises(Exception, match="earlier index"):
        contract.review_duplicate(root, child)
    assert contract.review_count() == 1


def test_cross_operator_and_unclear_review_leave_tickets_open(direct_vm, direct_deploy, direct_bob):
    contract = direct_deploy("repair_merge.py")
    first = contract.file_report("SITE-1", 10, "Unknown door.")
    second = contract.file_report("SITE-1", 11, "Some latch sticks.")
    with direct_vm.prank(direct_bob), pytest.raises(Exception, match="only the reports operator"):
        contract.review_duplicate(second, first)
    direct_vm.mock_llm("untrusted facilities work-order", "UNCLEAR")
    assert contract.review_duplicate(second, first) == "UNCLEAR"
    assert json.loads(contract.get_report(second))["duplicate_of"] is None
    assert json.loads(contract.get_review(0))["outcome"] == "UNCLEAR"
