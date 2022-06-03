from dataclasses import dataclass

from vm.opcode import Opcode
from vm.pc import ProgramCounter
from vm.scope_ctx import  ScopeContext

def opAdd(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    x, y = scope_ctx.stack.pop(), scope_ctx.stack.pop()
    z = x + y

    scope_ctx.stack.push(z)

def opSub(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    x, y = scope_ctx.stack.pop(), scope_ctx.stack.pop()
    z = x - y

    scope_ctx.stack.push(z)

def opPush1(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    ## 1. get 1 byte immediate value & update PC properly

    pc.increment()

    push_value: bytes = scope_ctx.code[pc.get()] ## get next 1 BYTE

    ## 2. push immediate value to stack
    scope_ctx.stack.push(push_value)

@dataclass
class EVMInstruction:
    # Do we care about the N bytes next door?
    immediate_value: bool
    gas_cost: int
    execute: object


ReferenceTable: dict = {

    Opcode.PUSH1 : EVMInstruction(
        immediate_value=True,
        gas_cost=0,
        execute=opPush1,
    ), 

    Opcode.ADD : EVMInstruction(
        gas_cost=0,
        execute=opAdd,
    ),

    Opcode.SUB : EVMInstruction(
        gas_cost=0,
        execute=opSub,
    ),
}

