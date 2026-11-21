import pytest


@pytest.fixture(autouse=True)
def check_genvm_closures(direct_vm):
    direct_vm.check_pickling = True
