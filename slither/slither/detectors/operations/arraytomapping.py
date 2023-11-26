from typing import List
from slither.core.cfg.node import Node, NodeType
from slither.core.expressions.binary_operation import BinaryOperation
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.utils.output import Output
from slither import Slither
from slither.core.variables.state_variable import StateVariable
from slither.core.declarations.contract import Contract
from slither.core.solidity_types import ArrayType

from slither.core.declarations.contract import Contract
from slither.core.solidity_types import ArrayType

from slither import Slither

class ArrayToMapping(AbstractDetector):
    ARGUMENT = "array-to-mapping"
    HELP = (
        "Array to Mapping Detector"
    )
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.MEDIUM

    WIKI = "https://github.com/PereiraMavs/CSE6324_Team_8/wiki/Detector-Wiki#array-to-mapping"
    WIKI = "https://github.com/PereiraMavs/CSE6324_Team_8/wiki/Detector-Wiki#array-to-mapping"

    WIKI_TITLE = "Array to mapping"
    WIKI_DESCRIPTION = (
        "Detects Array usage in smart contracts and suggests to use map instead. "
    )
    WIKI_EXPLOIT_SCENARIO = " "
    WIKI_RECOMMENDATION = ("use solidity version 0.8.18 with slither")
    
    @staticmethod
    def _findArraysAndSuggestMaps(contract: Contract):
       issues = []

       #Iterate through the state variables of the contract:
       for state_variable in contract.variables:
           #Check if the state variable's type is an array (ArrayType):
           if (isinstance(state_variable.type, ArrayType)):
               #If an Array state variable is found, add it to the list of issues:
               issues.append(state_variable)
       return issues

   
    def _detect(self) -> List[Output]:
        results = []
       

        for contract in self.contracts:
            #Find array state variables in the contract:
            array_variables = self._findArraysAndSuggestMaps(contract)

            for array_variable in array_variables:
                #Generate a result for the detected issue:
                info = [f"In contract `{contract.name}`, for variable `{array_variable.name}`({array_variable.type}), consider using a mapping instead of an array."]
                res = self.generate_result(info)
                results.append(res)

        return results
    

