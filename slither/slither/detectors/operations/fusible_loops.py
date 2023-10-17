from typing import List
from slither.core.cfg.node import Node, NodeType
from slither.core.expressions.binary_operation import BinaryOperation
from slither.detectors.abstract_detector import AbstractDetector, DetectorClassification
from slither.utils.output import Output


class FusibleLoops(AbstractDetector):
    ARGUMENT = "fusible-loops"
    HELP = (
        "Detects `for` loops that can be merged into one loop. "
    )
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = "https://github.com/PereiraMavs/CSE6324_Team_8/wiki/Detector-Wiki#fusible-loops"

    WIKI_TITLE = "Find fusible loops"
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
    
    #entry point of the detector
    #calls the _findLoop function to find the loops that can be merged
    def _detect(self) -> List[Output]:
        results = []
        funtions = self.compilation_unit.functions
        
        issue = []
        for f in funtions:
            
            issue += FusibleLoops._findLoop(f.nodes, [])
            
        for i in issue:
            info = [
                "Loop condition ",
                i[0],
                i[1],
                " can be merged into one loop.\n",
            ]
            res = self.generate_result(info)
            results.append(res)
        return results
    