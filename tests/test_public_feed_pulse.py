import json

import pytest


def _watch(contract):
    return contract.open_watch("Library service map", "https://www.gov.uk/data", "https://www.usa.gov/services")


def _mock_pages(vm, pair):
    vm.mock_web(r"https://www\.(gov\.uk|usa\.gov)/", {"body": b"Public listing text."})
    vm.mock_llm("Read two public page extracts", pair)


def test_two_confirmations_and_loss_of_corroboration(direct_deploy, direct_vm):
    contract = direct_deploy("public_feed_pulse.py")
    watch = _watch(contract)
    _mock_pages(direct_vm, "LISTED,LISTED")
    contract.refresh(watch, 1)
    assert json.loads(contract.get_watch(watch))["status"] == "UNCONFIRMED"
    contract.refresh(watch, 2)
    assert json.loads(contract.get_watch(watch))["status"] == "LISTED"
    assert direct_vm.run_validator()
    assert not direct_vm.run_validator(leader_result="LISTED,UNKNOWN")
    direct_vm.clear_mocks()
    _mock_pages(direct_vm, "LISTED,PAUSED")
    contract.refresh(watch, 3)
    assert json.loads(contract.get_watch(watch))["status"] == "UNCONFIRMED"


def test_allowlist_ownership_rounds_and_missing_source(direct_deploy, direct_vm, direct_bob):
    contract = direct_deploy("public_feed_pulse.py")
    with pytest.raises(Exception, match="approved HTTPS"):
        contract.open_watch("Map", "https://localhost/a", "https://www.usa.gov/services")
    with pytest.raises(Exception, match="distinct hosts"):
        contract.open_watch("Map", "https://www.usa.gov/a", "https://www.usa.gov/b")
    watch = _watch(contract)
    with direct_vm.prank(direct_bob), pytest.raises(Exception, match="only the watch publisher"):
        contract.refresh(watch, 1)
    with pytest.raises(Exception, match="stale or skipped"):
        contract.refresh(watch, 2)
    direct_vm.mock_web("https://www.gov.uk/data", {"body": b"Library service map is published."})
    direct_vm.mock_llm("Read two public page extracts", "LISTED,LISTED")
    scan = json.loads(contract.get_scan(contract.refresh(watch, 1)))
    assert scan["source_states"] == ["LISTED", "UNREACHABLE"]
    assert scan["status"] == "UNCONFIRMED"
