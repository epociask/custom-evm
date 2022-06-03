from dataclasses import dataclass

from vm.opcode import Opcode
from vm.pc import ProgramCounter
from vm.scope_ctx import  ScopeContext

"""
Instruction logic taken from pseudocode presented in https://www.ethervm.io/ 
"""

def opAdd(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    x, y = scope_ctx.stack.pop(), scope_ctx.stack.pop()
    z = x + y

    scope_ctx.stack.push(z)

def opSub(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    x, y = scope_ctx.stack.pop(), scope_ctx.stack.pop()
    z = x - y

    scope_ctx.stack.push(z)

def opMul(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    x, y = scope_ctx.stack.pop(), scope_ctx.stack.pop()
    z = x * y

    scope_ctx.stack.push(z)

def opDiv(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    x, y = scope_ctx.stack.pop(), scope_ctx.stack.pop()
    z = x / y

    scope_ctx.stack.push(z)

def opMod(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    x, y = scope_ctx.stack.pop(), scope_ctx.stack.pop()
    z = x % y

    scope_ctx.stack.push(z)

def opAddMod(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    x, y, n = scope_ctx.stack.pop(), scope_ctx.stack.pop(), scope_ctx.stack.pop()
    z = (x+y) % n
    scope_ctx.stack.push(z)

def opMulMod(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    x, y, n = scope_ctx.stack.pop(), scope_ctx.stack.pop(), scope_ctx.stack.pop()
    z = (x*y) % n
    scope_ctx.stack.push(z)

def opExp(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    x, y = scope_ctx.stack.pop(), scope_ctx.stack.pop()
    z = x ** y

    scope_ctx.stack.push(z)


def opPush1(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    ## 1. get 1 byte immediate value & update PC properly

    pc.increment()

    push_value: bytes = scope_ctx.code[pc.get()] ## get next 1 BYTE

    ## 2. push immediate value to stack
    scope_ctx.stack.push(push_value)

@dataclass
class EVMInstruction:
    # Do we care about the 2 bytes next door?
    gas_cost: int
    execute: object


ReferenceTable: dict = {

    Opcode.PUSH1 : EVMInstruction(
        gas_cost=0,
        execute=opPush1,
    ), 

    Opcode.ADD : EVMInstruction(
        gas_cost=0,
        execute=opAdd,
    ),

    Opcode.MUL : EVMInstruction(
        gas_cost=0,
        execute=opMul,
    ),

    Opcode.SUB : EVMInstruction(
        gas_cost=0,
        execute=opSub,
    ),

    Opcode.DIV : EVMInstruction(
        gas_cost=0,
        execute=opDiv,
    ),

    Opcode.SDIV : EVMInstruction(
        gas_cost=0,
        execute=opDiv,
    ),

    Opcode.MOD : EVMInstruction(
        gas_cost=0,
        execute=opMod,
    ),

    Opcode.SMOD : EVMInstruction(
        gas_cost=0,
        execute=opMod,
    ),

   Opcode.ADDMOD : EVMInstruction(
        gas_cost=0,
        execute=opAddMod,
    ),

   Opcode.MULMOD : EVMInstruction(
        gas_cost=0,
        execute=opMulMod,
    ),

    Opcode.EXP : EVMInstruction(
        gas_cost=0,
        execute=opExp,
    )



}

