from vm.contract import Contract
from vm.memory import Memory
from vm.stack import Stack
from vm.pc import ProgramCounter
from vm.opcode import Opcode
from vm.instructions import ReferenceTable
from vm.machine_ctx import MachineContext
from vm.constants import (
    CompletedExecution,
    ReturnCode
)


class EVMInterpreter:

    def __init__(self, storage):
        self.scope_ctx = None
        self.storage = storage

    def run(self, contract: Contract) -> CompletedExecution:
        
        stack, mem = Stack(), Memory()

        ctx = MachineContext(contract, mem, stack)
        self.scope_ctx = ctx

        pc = ProgramCounter(0)

        ## Main execution loop ## 

        while True:
            op: Opcode = contract.get_op(pc)
            print(f"PC = {pc.get()}, OP = {repr(op)}")
            
            if op == Opcode.STOP:
                return CompletedExecution(code=ReturnCode.STOPPED, data=None)

            if op == Opcode.REVERT:
                return CompletedExecution(code=ReturnCode.REVERTED, data=None)

            ReferenceTable[op].execute(pc, self, ctx)
            print(f"Stack -> {ctx.stack}")

            ## move to next byte in instruction encoding
            pc.increment(amount=1)