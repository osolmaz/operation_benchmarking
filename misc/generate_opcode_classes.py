# This script can be used to generate Operation classes for WASM opcodes once
# the module `operation_benchmarking` is installed

from operation_benchmarking.operations.wasm_opcodes import OPCODE_NAMES

ofile = open("out.py", "w")

for name in OPCODE_NAMES:
    ofile.write("class %sOperation(ConstantOperation):\n"%name)
    ofile.write("    def get_name(self):\n")
    ofile.write("        return \"%s\"\n"%name)
    ofile.write("\n\n")

