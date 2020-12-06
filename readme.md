# permit-deposit

Deposit into Yearn Vaults in a single transaction using a approvals by signature.

Available for tokens which implement `permit`.
See also [EIP-2612](https://eips.ethereum.org/EIPS/eip-2612).

## DAI

Mainnet deployment: [`0xF6f4526a05a38198dBEddFc226d30dbb5419951F`](https://etherscan.io/address/0xF6f4526a05a38198dBEddFc226d30dbb5419951F#code) for `0xBFa4D8AA6d8a379aBFe7793399D3DdaCC5bBECBB`

`deposit(uint amount, Permit permit)`

where `Permit` is a signed permit for DAI contract

`(address holder, address spender, uint256 nonce, uint256 expiry, bool allowed, uint8 v, bytes32 r, bytes32 s)`

Learn how to construct a permit [using web3.js](https://github.com/makerdao/developerguides/blob/master/dai/how-to-use-permit-function/how-to-use-permit-function.md) or [using python](tests/test_dai_permit.py).

## USDC

Mainnet deployment: [0x8cd1675776fA1C1377E60EB3f47D3C8857630052](https://etherscan.io/address/0x8cd1675776fA1C1377E60EB3f47D3C8857630052#code) for `0xe2F6b9773BF3A015E2aA70741Bde1498bdB9425b`

`deposit(uint amount, Permit permit)`

where `Permit` is a signer permit for USDC contract

`(address owner, address spender, uint256 value, uint256 nonce, uint256 deadline, uint8 v, bytes32 r, bytes32 s)`

Learn how to construct a permit [using python](tests/test_usdc_permit.py).

Relevant contract [source code](https://github.com/centrehq/centre-tokens/blob/master/contracts/v2/Permit.sol).
