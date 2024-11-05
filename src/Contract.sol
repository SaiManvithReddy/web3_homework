// SPDX-License-Identifier: MIT
pragma solidity 0.8.13;

contract newContract {
    uint public StudentId;
    address public owner;

    constructor() public {
        StudentId = 10;
        owner = msg.sender;
    }

    function viewMyId() public view returns (uint) {
        return StudentId;
    }

    function updateID(uint _newId) public {
        require(msg.sender == owner);
        StudentId = _newId;
    }
}
