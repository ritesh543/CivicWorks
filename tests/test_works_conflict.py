import json

import pytest


def test_adjacent_closed_windows_skip_model(direct_deploy):
    contract = direct_deploy("works_conflict.py")
    index = contract.compare("Oak Road", 10, 20, True, "Oak Road", 20, 30, True)
    report = json.loads(contract.get_check(index))
    assert report["overlap_window"] == []
    assert report["outcome"] == "NO_TIME_OVERLAP"
    with pytest.raises(Exception, match="invalid first window"):
        contract.compare("Oak Road", 20, 20, True, "Oak Road", 20, 30, True)
    assert contract.count() == 1


@pytest.mark.parametrize(
    ("relation", "both_full", "expected"),
    [("SAME", True, "FULL_CONFLICT"), ("SAME", False, "COORDINATE"),
     ("SEPARATE", True, "SEPARATE_SEGMENTS"), ("UNCLEAR", True, "REVIEW_LOCATION")],
)
def test_overlap_and_location_have_distinct_effects(direct_vm, direct_deploy, relation, both_full, expected):
    contract = direct_deploy("works_conflict.py")
    direct_vm.mock_llm("Compare the two public roadwork", relation)
    index = contract.compare("Oak, 1st to 3rd", 10, 40, True, "Oak, 2nd to 4th", 20, 50, both_full)
    report = json.loads(contract.get_check(index))
    assert report["overlap_window"] == [20, 40]
    assert report["outcome"] == expected
    assert direct_vm.run_validator()
    other = "SAME" if relation != "SAME" else "UNCLEAR"
    assert not direct_vm.run_validator(leader_result=other)
