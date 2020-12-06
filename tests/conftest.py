import pytest


@pytest.fixture(scope="function", autouse=True)
def shared_setup(fn_isolation):
    pass


@pytest.fixture
def dai(interface, dai_whale):
    return interface.Dai("0x6B175474E89094C44Da98b954EedeAC495271d0F", owner=dai_whale)


@pytest.fixture
def dai_whale(accounts):
    return accounts.at("0xA478c2975Ab1Ea89e8196811F51A7B7Ade33eB11", force=True)


@pytest.fixture
def dai_vault(TestVault, dai, accounts):
    return TestVault.deploy(dai, {"from": accounts[0]})


@pytest.fixture
def dai_deposit(DaiVaultPermitDeposit, dai_vault, accounts):
    return DaiVaultPermitDeposit.deploy(dai_vault, {"from": accounts[0]})


@pytest.fixture
def usdc(interface, usdc_whale):
    return interface.FiatTokenV2(
        "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", owner=usdc_whale
    )


@pytest.fixture
def usdc_whale(accounts):
    return accounts.at("0xA191e578a6736167326d05c119CE0c90849E84B7", force=True)


@pytest.fixture
def usdc_vault(TestVault, usdc, accounts):
    return TestVault.deploy(usdc, {"from": accounts[0]})


@pytest.fixture
def usdc_deposit(UsdcVaultPermitDeposit, usdc_vault, accounts):
    return UsdcVaultPermitDeposit.deploy(usdc_vault, {"from": accounts[0]})
