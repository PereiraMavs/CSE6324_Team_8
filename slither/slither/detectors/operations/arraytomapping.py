from typing import List
from slither.core.cfg.node import Node, NodeType
from slither.core.expressions.binary_operation import BinaryOperation
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.utils.output import Output
from slither import Slither
#from slither.solc_parsing.variables.state import StateVariable
from slither.core.variables.state_variable import StateVariable
from slither import Slither

class ArrayToMapping(AbstractDetector):
    ARGUMENT = "array-to-mapping"
    HELP = (
        "Array to Mapping Detector "
    )
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.MEDIUM

    WIKI = "https://github.com/PereiraMavs/CSE6324_Team_8/wiki/Detector-Wiki#fusible-loops"

    WIKI_TITLE = "Array to mapping"
    WIKI_DESCRIPTION = (
        "Detects `for` loops that can be merged into one loop. "
    )
    WIKI_EXPLOIT_SCENARIO = " "
    WIKI_RECOMMENDATION = ("use solidity version 0.8.18 with slither")
    
    #finds the loops that can be merged
    #returns a list of tuples of the loops that can be merged
    #the tuple contains the nodes of the loops
    #the first node of the tuple is the first loop
    #the second node of the tuple is the second loop
    @staticmethod
    def _findLoop(nodes: List[Node], fuse: List[Node]):
        visited = []
        
        for node in nodes:
            if node.type == NodeType.STARTLOOP:
                if_node = node.sons[0]
                
                exp: BinaryOperation = if_node.expression
                visited.append(node)
        for i in range(0,len(visited)):
            for i2 in range(i + 1,len(visited)):
                n1: Node = visited[i]
                n2: Node = visited[i2]
                e1: BinaryOperation = n1.sons[0].expression
                e2: BinaryOperation = n2.sons[0].expression
                if str(e1.expression_right) == str(e2.expression_right):
                    fuse.append((n1, n2))
                    
        return fuse
    


def  detect_array_usage(self):
    issues = []

    for contract in self.contracts:
        for state_variable in contract.variables:
                if isinstance(state_variable, StateVariable) and state_variable.array:
                    issues.append((contract.name, state_variable.name, state_variable.type, state_variable.source_mapping))
        
    return issues

   
def _detect(self) -> List[Output]:
    results = []
      
    
    issues = detect_array_usage(self)

    for issue in issues:
        contract_name, variable_name, variable_type, source_mapping = issue

        info = [
                "In contract ",
                f"`{contract_name}` ",
                "consider using a mapping instead of array for",
                f"{variable_name} ",
                f"({variable_type})",
            ]
        #print(f"In contract '{contract_name}', consider using a mapping instead of array for '{variable_name}' ({variable_type}).")
        #print(f"Location: {source_mapping}")


        res = self.generate_result(info)
        results.append(res)
    return results
    