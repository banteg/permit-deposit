import pytest


@pytest.fixture(scope="function", autouse=True)
def shared_setup(fn_isolation):
    pass


@pytest.fixture
def dai_vault(interface, accounts):
    vault = interface.Vault("0xBFa4D8AA6d8a379aBFe7793399D3DdaCC5bBECBB")
    governance = accounts.at(vault.governance(), force=True)
    vault.setGuestList("0x" + "00" * 20, {"from": governance})
    return vault


@pytest.fixture
def dai(interface, dai_whale):
    return interface.Dai("0x6B175474E89094C44Da98b954EedeAC495271d0F", owner=dai_whale)


@pytest.fixture
def dai_deposit(DaiVaultPermitDeposit, dai_vault, accounts):
    return DaiVaultPermitDeposit.deploy(dai_vault, {"from": accounts[0]})


@pytest.fixture
def dai_whale(accounts):
    return accounts.at("0xA478c2975Ab1Ea89e8196811F51A7B7Ade33eB11", force=True)
