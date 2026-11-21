import json

import pytest


def test_complete_notice_still_has_an_exact_lead_time_gate(direct_vm, direct_deploy):
    contract = direct_deploy("notice_clock.py", 120)
    direct_vm.mock_llm("Review a public service-change notice", "COMPLETE")
    label = "Nov 22 at 10:00 UTC"
    scope = "Oak library west door closes"
    notice = f"Oak library west door closes {label}."
    threshold = contract.check(scope, label, 100, 220, notice)
    late = contract.check(scope, label, 101, 220, notice)
    backdated = contract.check(scope, label, 221, 220, notice)
    assert json.loads(contract.get_report(threshold))["passes"] is True
    assert json.loads(contract.get_report(late))["passes"] is False
    assert json.loads(contract.get_report(backdated))["lead_minutes"] == -1
    assert not direct_vm.run_validator(leader_result="INCOMPLETE")


def test_early_notice_with_missing_content_fails(direct_vm, direct_deploy):
    contract = direct_deploy("notice_clock.py", 120)
    direct_vm.mock_llm("Review a public service-change notice", "INCOMPLETE")
    result = json.loads(contract.get_report(contract.check("Library closes", "10 am", 0, 200, "See you soon.")))
    assert result["lead_satisfied"] and not result["passes"]


def test_constructor_rejects_zero_lead(direct_deploy):
    with pytest.raises(Exception, match="minimum lead"):
        direct_deploy("notice_clock.py", 0)
