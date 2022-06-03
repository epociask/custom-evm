from dataclasses import dataclass

from vm.contract import Contract
from vm.memory import Memory
from vm.stack import Stack
from vm.pc import ProgramCounter
from vm.opcode import Opcode
from vm.instructions import ReferenceTable
from vm.scope_ctx import ScopeContext


class EVMInterpreter:
    scope_ctx = None

    def run(self, contract: Contract):
        
        stack, mem = Stack(), Memory()

        call_ctx = ScopeContext(contract.code, mem, stack)
        self.scope_ctx = call_ctx

        pc = ProgramCounter(0)

        ## Main execution loop

        while True:
            op: Opcode = contract.get_op(pc)

            if op == Opcode.STOP:
                break

            print(f"PC = {pc.get()}, OP = {repr(op)}")
            
            ReferenceTable[op].execute(pc, self, call_ctx)
            print(f"Stack -> {call_ctx.stack}")

            ## move to next byte in instruction encoding
            pc.increment(amount=1)