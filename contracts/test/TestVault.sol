// SPDX-License-Identifier: AGPLv3
pragma solidity =0.6.12;

interface ERC20 {
    function transferFrom(
        address from,
        address to,
        uint256 value
    ) external returns (bool);
}

contract TestVault {
    ERC20 public token;
    mapping(address => uint256) public balanceOf;

    constructor(address _token) public {
        token = ERC20(_token);
    }

    function deposit(uint256 amount, address recipient) public returns (bool) {
        token.transferFrom(msg.sender, address(this), amount);
        balanceOf[recipient] += amount;
        return true;
    }
}
