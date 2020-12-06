from eth_account import Account
from eth_account._utils.structured_data.hashing import hash_domain
from eth_account.messages import encode_structured_data
from eth_utils import encode_hex


def build_permit(owner, spender, value, deadline, usdc):
    data = {
        "types": {
            "EIP712Domain": [
                {"name": "name", "type": "string"},
                {"name": "version", "type": "string"},
                {"name": "chainId", "type": "uint256"},
                {"name": "verifyingContract", "type": "address"},
            ],
            "Permit": [
                {"name": "owner", "type": "address"},
                {"name": "spender", "type": "address"},
                {"name": "value", "type": "uint256"},
                {"name": "nonce", "type": "uint256"},
                {"name": "deadline", "type": "uint256"},
            ],
        },
        "domain": {
            "name": "USD Coin",
            "version": "2",
            "chainId": 1,
            "verifyingContract": str(usdc),
        },
        "primaryType": "Permit",
        "message": {
            "owner": owner,
            "spender": spender,
            "value": value,
            "nonce": usdc.nonces(owner),
            "deadline": deadline,
        },
    }
    assert encode_hex(hash_domain(data)) == usdc.DOMAIN_SEPARATOR()
    return encode_structured_data(data)


def test_usdc_permit(usdc, usdc_deposit):
    signer = Account.create()
    owner = signer.address
    value = 1000 * 10 ** usdc.decimals()
    deadline = 2 ** 256 - 1
    permit = build_permit(owner, str(usdc_deposit), value, deadline, usdc)
    signed = signer.sign_message(permit)
    usdc.permit(owner, usdc_deposit, value, deadline, signed.v, signed.r, signed.s)
    assert usdc.allowance(owner, usdc_deposit) == value


def test_usdc_permit_deposit(usdc, usdc_vault, usdc_deposit):
    signer = Account.create()
    owner = signer.address
    value = 1000 * 10 ** usdc.decimals()
    deadline = 2 ** 256 - 1
    usdc.transfer(owner, value)
    assert usdc.balanceOf(owner) == value
    permit = build_permit(owner, str(usdc_deposit), value, deadline, usdc)
    signed = signer.sign_message(permit)
    usdc_deposit.deposit(
        value, [owner, usdc_deposit, value, deadline, signed.v, signed.r, signed.s]
    )
    assert usdc_vault.balanceOf(owner) > 0
    print(usdc_vault.balanceOf(owner) / 10 ** usdc.decimals())
