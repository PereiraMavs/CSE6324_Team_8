// SPDX-License-Identifier: MIT
pragma solidity ^0.8.18;

contract ArrayUsageExample {
    uint[] public dynamicArray;
    uint[5] public fixedArray;
    mapping(address => uint) public map;

    constructor() {
        dynamicArray.push(1);
        dynamicArray.push(2);
        dynamicArray.push(3);

        fixedArray[0] = 10;
        fixedArray[1] = 20;
        fixedArray[2] = 30;

        map[msg.sender] = 100;
    }

    function addValueToDynamicArray(uint _value) public {
        dynamicArray.push(_value);
    }

    function getValueFromDynamicArray(uint _index) public view returns (uint) {
        require(_index < dynamicArray.length, "Index out of bounds");
        return dynamicArray[_index];
    }
}

