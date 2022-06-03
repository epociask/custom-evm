from vm.pc import ProgramCounter
from vm.opcode import Opcode

class Contract:        
    #TODO add jumping logic
    ## IE jump destination mapping && analysis logic
    code: list = []
    _input: list = []

    def __init__(self, code, _input):
        self.code = code
        self._input = _input

    def get_op(self, pc: ProgramCounter) -> Opcode:
        if pc.get() >= len(self.code): ## attempting execution of value of bounds
            return Opcode.STOP

        return Opcode(self.code[pc.get()])