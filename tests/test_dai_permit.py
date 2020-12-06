from eth_account import Account
from eth_account._utils.structured_data.hashing import hash_domain
from eth_account.messages import encode_structured_data
from eth_utils import encode_hex


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


def test_dai_permit(dai, dai_deposit):
    signer = Account.create()
    holder = signer.address
    permit = build_permit(holder, str(dai_deposit), dai)
    signed = signer.sign_message(permit)
    dai.permit(holder, dai_deposit, 0, 0, True, signed.v, signed.r, signed.s)
    assert dai.allowance(holder, dai_deposit) == 2 ** 256 - 1


def test_dai_permit_deposit(dai, dai_vault, dai_deposit):
    signer = Account.create()
    holder = signer.address
    amount = "1000 ether"
    dai.transfer(holder, amount)
    assert dai.balanceOf(holder) == amount
    permit = build_permit(holder, str(dai_deposit), dai)
    signed = signer.sign_message(permit)
    dai_deposit.deposit(
        amount, [holder, dai_deposit, 0, 0, True, signed.v, signed.r, signed.s]
    )
    assert dai.allowance(holder, dai_deposit) == 2 ** 256 - 1
    assert dai_vault.balanceOf(holder) > 0
    print(dai_vault.balanceOf(holder).to("ether"))
