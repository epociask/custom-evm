from dataclasses import dataclass
import numpy

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

def opJump(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    dest = scope_ctx.stack.pop()
    pc.set(dest)

def opJumpDest(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    pass

def opLt(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    a, b = scope_ctx.stack.pop(), scope_ctx.stack.pop()
    c = (a < b)

    scope_ctx.stack.push(c)

def opGt(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    a, b = scope_ctx.stack.pop(), scope_ctx.stack.pop()
    c = (a > b)

    scope_ctx.stack.push(c)

def opEq(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    a, b = scope_ctx.stack.pop(), scope_ctx.stack.pop()
    c = (a == b)

    scope_ctx.stack.push(c)

def opIsZero(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    a = scope_ctx.stack.pop()
    c = (a == 0)

    scope_ctx.stack.push(c)

def opAnd(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    a, b = scope_ctx.stack.pop(), scope_ctx.stack.pop()
    c = (a & b) #bitwise and

    scope_ctx.stack.push(c)

def opOr(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    a, b = scope_ctx.stack.pop(), scope_ctx.stack.pop()
    c = (a | b) #bitwise or

    scope_ctx.stack.push(c)

def opXor(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    a, b = scope_ctx.stack.pop(), scope_ctx.stack.pop()
    c = (a ^ b)

    scope_ctx.stack.push(c)

def opNot(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    a = scope_ctx.stack.pop()
    c = not(a)
    
    scope_ctx.stack.push(c)

def opByte(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    i, x = scope_ctx.stack.pop(), scope_ctx.stack.pop()
    y = (x >> (248 - i * 8)) & 0xFF

    scope_ctx.stack.push(y)

def opShl(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    shift, value = scope_ctx.stack.pop(), scope_ctx.stack.pop()
    result = numpy.left_shift(value, shift)

    scope_ctx.stack.push(result)

def opShr(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    shift, value = scope_ctx.stack.pop(), scope_ctx.stack.pop()
    result = numpy.right_shift(value, shift)

    scope_ctx.stack.push(result)

def opSar(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    shift, value = scope_ctx.stack.pop(), scope_ctx.stack.pop()
    result = value >> shift

    scope_ctx.stack.push(result)

def opSha3(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    pass

def opPush1(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    ## 1. get 1 byte immediate value & update PC properly

    pc.increment()

    push_value: bytes = scope_ctx.code[pc.get()] ## get next 1 BYTE

    ## 2. push immediate value to stack
    scope_ctx.stack.push(push_value)

@dataclass
class EVMInstruction:
    # Do we care about the N bytes next door?
    gas_cost: int
    execute: object

    immediate_value: bool=False
    immediate_size: int=0

ReferenceTable: dict = {

    Opcode.PUSH1 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
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
    ),


    Opcode.JUMP : EVMInstruction(
        gas_cost=0,
        execute=opJump,
    ),

    Opcode.JUMPDEST : EVMInstruction(
        gas_cost=0,
        execute=opJumpDest,
    ),

    Opcode.LT : EVMInstruction(
        gas_cost=0,
        execute=opLt,
    ),

    Opcode.GT : EVMInstruction(
        gas_cost=0,
        execute=opGt,
    ),

    Opcode.EQ : EVMInstruction(
        gas_cost=0,
        execute=opEq,
    ),

    Opcode.ISZERO : EVMInstruction(
        gas_cost=0,
        execute=opIsZero,
    ),

    Opcode.AND : EVMInstruction(
        gas_cost=0,
        execute=opAnd,
    ),

    Opcode.OR : EVMInstruction(
        gas_cost=0,
        execute=opOr,
    ),

    Opcode.XOR : EVMInstruction(
        gas_cost=0,
        execute=opXor,
    ),

    Opcode.NOT : EVMInstruction(
        gas_cost=0,
        execute=opNot,
    ),

    Opcode.BYTE : EVMInstruction(
        gas_cost=0,
        execute=opByte,
    ),

    Opcode.SHL : EVMInstruction(
        gas_cost=0,
        execute=opShl,
    ),

    Opcode.SHR : EVMInstruction(
        gas_cost=0,
        execute=opShr,
    ),

    Opcode.SAR : EVMInstruction(
        gas_cost=0,
        execute=opSar,
    )
}

