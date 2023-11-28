from slither.printers.abstract_printer import AbstractPrinter
from slither.utils.output import Output
import subprocess
import pandas as pd


def get_opcode_list():
    data_file = 'opcodes.xlsx'
    df = pd.read_excel(data_file)
    key = 'OPCODE'
    value= 'VALUE'
    op_dict = dict(zip(df[key], df[value]))
    return op_dict

def calculate(code, dct:dict):
    s_code = code.split(' ')
    gas = 0
    for op in range(1, len(s_code)-1):
        res = dct.get(s_code[op])
        if res is not None:
            gas= gas + res
    return gas

class CalculateGas(AbstractPrinter):
    ARGUMENT = "calc-gas"
    HELP = "Calculate Gas"

    WIKI = "https://github.com/trailofbits/slither/wiki/Printer-documentation#"

    # Printer to find gas value from used opcodes
    def output(self, filename: str) -> Output:
        catch = subprocess.run(['solc', '--opcodes', filename], capture_output=True)
        info = str(catch.stdout)
        gas = calculate(info, get_opcode_list())
        final = "Minimum gas required " + str(gas)
        self.info(final)
        res = self.generate_output(final)
        return res