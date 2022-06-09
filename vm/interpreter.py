from vm.contract import Contract
from vm.memory import Memory
from vm.stack import Stack
from vm.pc import ProgramCounter
from vm.opcode import Opcode
from vm.instructions import ReferenceTable
from vm.machine_ctx import MachineContext


class EVMInterpreter:
    scope_ctx = None

    def run(self, contract: Contract):
        
        stack, mem = Stack(), Memory()

        ctx = MachineContext(contract.code, mem, stack)
        self.scope_ctx = ctx

        pc = ProgramCounter(0)

        ## Main execution loop ## 

        while True:
            op: Opcode = contract.get_op(pc)

            if op == Opcode.STOP:
                break

            print(f"PC = {pc.get()}, OP = {repr(op)}")
            
            ReferenceTable[op].execute(pc, self, ctx)
            print(f"Stack -> {ctx.stack}")

            ## move to next byte in instruction encoding
            pc.increment(amount=1)