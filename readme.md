# permit-deposit

Deposit into Yearn Vaults in a single transaction using a approvals by signature.

Available for tokens which implement `permit`.
See also [EIP-2612](https://eips.ethereum.org/EIPS/eip-2612).

## DAI

`deposit(uint amount, Permit permit)`

where `Permit` is a signed permit for DAI contract

`(address holder, address spender, uint256 nonce, uint256 expiry, bool allowed, uint8 v, bytes32 r, bytes32 s)`

Learn how to construct a permit [using web3.js](https://github.com/makerdao/developerguides/blob/master/dai/how-to-use-permit-function/how-to-use-permit-function.md) or [using python](tests/test_dai_permit.py).

## USDC

`deposit(uint amount, Permit permit)`

where `Permit` is a signer permit for USDC contract

`(address owner, address spender, uint256 value, uint256 nonce, uint256 deadline, uint8 v, bytes32 r, bytes32 s)`

Learn how to construct a permit [using python](tests/test_usdc_permit.py).

Relevant contract [source code](https://github.com/centrehq/centre-tokens/blob/master/contracts/v2/Permit.sol).
