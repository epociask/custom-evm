from vm.pc import ProgramCounter
from vm.opcode import Opcode

class Contract:        
    ## TODO jump destination mapping && analysis logic
    code: bytearray = []
    data: bytearray = []
    value: int = 0

    def __init__(self, code, data, value=0):
        self.code = code
        self.data = data
        self.value = value

    def get_op(self, pc: ProgramCounter) -> Opcode:
        if pc.get() >= len(self.code): ## attempting execution OUT OF BOUNDS
            return Opcode.STOP

        return Opcode(self.code[pc.get()])