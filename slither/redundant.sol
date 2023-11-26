// SPDX-License-Identifier: MIT
pragma solidity ^0.8.18;

contract RedundantExample {
    uint baseprice;
    uint check;
    uint another = 0;
    function setBasePrice(uint new_baseprice) public {
        baseprice = new_baseprice;
        for(uint i = 0; i < new_baseprice; i++) {
            check = new_baseprice + i;
        }

        if (new_baseprice > 10) {
            baseprice = baseprice + 1;
        }
    }
}