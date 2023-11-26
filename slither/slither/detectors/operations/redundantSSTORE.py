from typing import List, Optional, Dict

from slither.core.compilation_unit import SlitherCompilationUnit
from slither.core.declarations import Function
from slither.core.declarations.contract import Contract
from slither.core.solidity_types import ArrayType
from slither.core.variables import Variable
from slither.core.variables.state_variable import StateVariable
from slither.detectors.abstract_detector import (
    AbstractDetector,
    DetectorClassification,
    DETECTOR_INFO,
)
from slither.formatters.variables.unused_state_variables import custom_format
from slither.utils.output import Output
from slither.visitors.expression.export_values import ExportValues

# Function to find out redundant SSTORE operation
def detect_redundant_write(contract: Contract) -> Optional[List[StateVariable]]:
    
    # Get the list of all functions
    all_functions = [
        f
        for f in contract.functions + list(contract.modifiers)
        if isinstance(f, Function)
    ]

    # Get a list of variables read/written in each function separately
    variables_read = [x.state_variables_read for x in all_functions]
    variables_written = [x.state_variables_written for x in all_functions]
    
    # Convert previous arrays to one dimensional lists
    read = [x for y in variables_read for x in y]
    written = [x for y in variables_written for x in y]
    
    # Return the list variables which are written to but not read
    return [x for x in written if x not in read]


class redundantSSTORE(AbstractDetector):

    ARGUMENT = "redundant-store"
    HELP = "variables only written but never used"
    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.MEDIUM

    WIKI = "https://github.com/crytic/slither/wiki/Detector-Documentation#redundant-store"

    WIKI_TITLE = "Redundant SSTORE operation"
    WIKI_DESCRIPTION = "No read after write causing costly SSTORE operation redundant"
    WIKI_EXPLOIT_SCENARIO = ""
    WIKI_RECOMMENDATION = "Use or remove redundant write operation"

    def _detect(self) -> List[Output]:
        results = []
        for c in self.compilation_unit.contracts_derived:
            if c.is_signature_only():
                continue
            unusedVars = detect_redundant_write(c)
            if unusedVars:
                for var in unusedVars:
                    info: DETECTOR_INFO = [var, " is written but not read ", c, "\n"]
                    g_info = self.generate_result(info)
                    results.append(g_info)
        return results