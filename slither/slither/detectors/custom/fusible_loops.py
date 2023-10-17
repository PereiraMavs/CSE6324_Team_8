from typing import List
from slither.detectors.abstract_detector import AbstractDetector

from slither.detectors.abstract_detector import DetectorClassification
from slither.utils.output import Output


class FusibleLoops(AbstractDetector):
    ARGUMENT = "fusible-loops"
    HELP = (
        "Detects any loops which can be fused into a single loop. "
    )
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI = "https://github.com/crytic/slither/wiki/Detector-Documentation#cache-array-length"

    WIKI_TITLE = "Fuse mutlple loops"
    WIKI_DESCRIPTION = (
        "Detects `for` loops that "
    )
    WIKI_EXPLOIT_SCENARIO = ""
    WIKI_RECOMMENDATION = ("this is a suggestion for developers preference")
    
    
    def _detect(self) -> List[Output]:
        results = []
        info = [
                "Loop condition ",
                "test",
                "test",
                "should use cached array length instead of referencing `length` member "
                "of the storage array.\n ",
            ]
        
        results.append(info)
        return results