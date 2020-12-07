from brownie import accounts, interface, DaiVaultPermitDeposit, Wei
from eth_account import Account
from eth_account._utils.structured_data.hashing import hash_domain
from eth_account.messages import encode_structured_data
from eth_utils import encode_hex
import click


def build_permit(holder, spender, dai):
    data = {
        "types": {
            "EIP712Domain": [
                {"name": "name", "type": "string"},
                {"name": "version", "type": "string"},
                {"name": "chainId", "type": "uint256"},
                {"name": "verifyingContract", "type": "address"},
            ],
            "Permit": [
                {"name": "holder", "type": "address"},
                {"name": "spender", "type": "address"},
                {"name": "nonce", "type": "uint256"},
                {"name": "expiry", "type": "uint256"},
                {"name": "allowed", "type": "bool"},
            ],
        },
        "domain": {
            "name": dai.name(),
            "version": dai.version(),
            "chainId": 1,
            "verifyingContract": str(dai),
        },
        "primaryType": "Permit",
        "message": {
            "holder": holder,
            "spender": spender,
            "nonce": dai.nonces(holder),
            "expiry": 0,
            "allowed": True,
        },
    }
    assert encode_hex(hash_domain(data)) == dai.DOMAIN_SEPARATOR()
    return encode_structured_data(data)


def main():
    dai = interface.Dai("0x6B175474E89094C44Da98b954EedeAC495271d0F")
    dai_deposit = DaiVaultPermitDeposit.at("0xF6f4526a05a38198dBEddFc226d30dbb5419951F")
    dai_vault = interface.Vault("0xBFa4D8AA6d8a379aBFe7793399D3DdaCC5bBECBB")
    user = accounts.load(click.prompt("Account", type=click.Choice(accounts.load())))
    signer = Account.from_key(user.private_key)
    balance = dai.balanceOf(user)
    print("DAI balance:", balance.to("ether"))
    amount = click.prompt("Deposit amount", type=click.FloatRange(min=0))
    amount = min(Wei(f"{amount} ether"), balance)
    permit = build_permit(str(user), str(dai_deposit), dai)
    signed = signer.sign_message(permit)
    if click.confirm("Send transaction?"):
        dai_deposit.deposit(
            amount,
            [user, dai_deposit, 0, 0, True, signed.v, signed.r, signed.s],
            {"from": user},
        )
    vault_balance = dai_vault.balanceOf(user)
    print("yvDAI balance", vault_balance.to("ether"))
