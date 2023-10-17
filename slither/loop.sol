// SPDX-License-Identifier: MIT
pragma solidity ^0.8.18;

contract Loop {
    function loop() public pure {
        // for loops with similar iteration conditions
        uint n = 10;
        for (uint i = 0; i < n; i++) {
            if (i == 3) {
                continue;
            }
            if (i == 5) {
                break;
            }
        }
        
        for (uint i = 0; i < n; i++) {
            if (i == 3) {
                continue;
            }
        }
    }
}

