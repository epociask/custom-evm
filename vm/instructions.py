from dataclasses import dataclass
import numpy
import sha3

from vm.opcode import Opcode
from vm.pc import ProgramCounter
from vm.scope_ctx import  ScopeContext
from vm.constants import (
    MAX_UINT_256,
    MAX_256_HEX
    )

"""
Instruction logic taken from pseudocode presented in:
    * https://www.ethervm.io/ 
    * https://ethereum.org/en/developers/docs/evm/opcodes/
"""


##                                   ##
#   Instruction defintion functions   #
##                                   ##
def opAdd(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    x, y = scope_ctx.stack.pop(), scope_ctx.stack.pop()
    z: int = x + y

    scope_ctx.stack.push(z)

def opSub(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    x, y = scope_ctx.stack.pop(), scope_ctx.stack.pop()
    z: int = x - y

    scope_ctx.stack.push(z)

def opMul(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    x, y = scope_ctx.stack.pop(), scope_ctx.stack.pop()
    z: int = x * y

    scope_ctx.stack.push(z)

def opDiv(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    x, y = scope_ctx.stack.pop(), scope_ctx.stack.pop()
    z = x / y

    scope_ctx.stack.push(z)

def opMod(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    x, y = scope_ctx.stack.pop(), scope_ctx.stack.pop()
    z: int = x % y

    scope_ctx.stack.push(z)

def opAddMod(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    x, y, n = scope_ctx.stack.pop(), scope_ctx.stack.pop(), scope_ctx.stack.pop()
    z: int = (x+y) % n
    scope_ctx.stack.push(z)

def opMulMod(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    x, y, n = scope_ctx.stack.pop(), scope_ctx.stack.pop(), scope_ctx.stack.pop()
    z: int = (x*y) % n
    scope_ctx.stack.push(z)

def opExp(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    x, y = scope_ctx.stack.pop(), scope_ctx.stack.pop()
    z: int = x ** y

    scope_ctx.stack.push(z)

def opJump(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    dest = scope_ctx.stack.pop()
    pc.set(dest)

def opJumpDest(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    pass

def opJumpI(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    dest, cond = scope_ctx.stack.pop(), scope_ctx.stack.pop()

    if cond:
        pc.set(dest)


def opLt(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    #TODO: Test me
    a, b = scope_ctx.stack.pop(), scope_ctx.stack.pop()
    c: bool = (a < b)

    scope_ctx.stack.push(c)

def opGt(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    #TODO: Test me
    a, b = scope_ctx.stack.pop(), scope_ctx.stack.pop()
    c: bool = (a > b)

    scope_ctx.stack.push(c)

def opEq(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    #TODO: Test me
    a, b = scope_ctx.stack.pop(), scope_ctx.stack.pop()
    c: bool = (a == b)

    scope_ctx.stack.push(c)

def opIsZero(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    #TODO: Test me
    a = scope_ctx.stack.pop()
    c: bool = (a == 0)

    scope_ctx.stack.push(c)

def opAnd(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    a, b = scope_ctx.stack.pop(), scope_ctx.stack.pop()
    c: bool = (a & b) #bitwise and

    scope_ctx.stack.push(c)

def opOr(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    a, b = scope_ctx.stack.pop(), scope_ctx.stack.pop()
    c: bool = (a | b) #bitwise or

    scope_ctx.stack.push(c)

def opXor(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    a, b = scope_ctx.stack.pop(), scope_ctx.stack.pop()
    c: bool = (a ^ b)

    scope_ctx.stack.push(c)

def opNot(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    a = scope_ctx.stack.pop()
    c: int = MAX_UINT_256 - a
    
    scope_ctx.stack.push(c)

def opByte(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    #TODO: Test me
    i, x = scope_ctx.stack.pop(), scope_ctx.stack.pop()
    y = (x >> (248 - i * 8)) & 0xFF

    scope_ctx.stack.push(y)

def opShl(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    shift, value = scope_ctx.stack.pop(), scope_ctx.stack.pop()
    
    if shift == MAX_256_HEX:
        result = 0
    else:
        result = numpy.left_shift(value, shift) & MAX_UINT_256

    scope_ctx.stack.push(result)

def opShr(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    #TODO: Test me
    shift, value = scope_ctx.stack.pop(), scope_ctx.stack.pop()
    result = numpy.right_shift(value, shift)

    scope_ctx.stack.push(result)

def opSar(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    #TODO: Test me
    shift, value = scope_ctx.stack.pop(), scope_ctx.stack.pop()
    result = value >> shift

    scope_ctx.stack.push(result)

def opSha3(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    #TODO: Test me
    offset = scope_ctx.stack.pop()
    value = scope_ctx.mem.get(offset)

    hasher = sha3.keccak_256()
    hasher.update(value)
    
    scope_ctx.push(hasher.hexidigest())

def opMload(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    offset = scope_ctx.stack.pop()
    val = scope_ctx.mem.get(offset)

    scope_ctx.stack.push(val)

def opMstore(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
    value, offset = scope_ctx.stack.pop(), scope_ctx.stack.pop()

    scope_ctx.mem.store(offset, value)

def makePushOp(byte_count: int):
    # TODO: test with 256 bit value 
    def pushN(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
        pc.increment()
        byte_val = scope_ctx.code[pc.get() : pc.get() + byte_count]
        int_val = int.from_bytes(byte_val, "big") #BIG Endian ordering man
        
        pc.increment(byte_count-1)
        scope_ctx.stack.push(int_val)


    return pushN

def makeDupOp(position: int):
    def dupN(pc: ProgramCounter, interp, scope_ctx: ScopeContext):
        scope_ctx.stack.duplicate(position-1)

    return dupN

@dataclass
class EVMInstruction:
    gas_cost: int
    execute: object

    immediate_value: bool=False
    immediate_size: int=0

##                                             ##
#   mapping for easy reference during execution #
##                                             ##
ReferenceTable: dict = {

    Opcode.PUSH1 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makePushOp(1),
    ),

    Opcode.PUSH2 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makePushOp(2),
    ), 

    Opcode.PUSH3 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makePushOp(3),
    ), 

    Opcode.PUSH4 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makePushOp(4),
    ), 

    Opcode.PUSH5 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makePushOp(5),
    ), 

    Opcode.PUSH6 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makePushOp(6),
    ), 

    Opcode.PUSH8 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makePushOp(8),
    ), 

    Opcode.PUSH9 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makePushOp(9),
    ), 

    Opcode.PUSH10 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makePushOp(10),
    ), 

    Opcode.PUSH11 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makePushOp(11),
    ), 

    Opcode.PUSH12 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makePushOp(12),
    ),

    Opcode.PUSH13 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makePushOp(13),
    ), 

    Opcode.PUSH14 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makePushOp(14),
    ), 

    Opcode.PUSH15 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makePushOp(15),
    ), 

    Opcode.PUSH16 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makePushOp(16),
    ), 

    Opcode.PUSH17 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makePushOp(17),
    ), 

    Opcode.PUSH18 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makePushOp(18),
    ), 

    Opcode.PUSH19 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makePushOp(19),
    ), 

    Opcode.PUSH20 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makePushOp(20),
    ), 

    Opcode.PUSH21 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makePushOp(21),
    ), 

    Opcode.PUSH22 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makePushOp(22),
    ), 

    Opcode.PUSH23 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makePushOp(23),
    ), 

    Opcode.PUSH24 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makePushOp(24),
    ), 

    Opcode.PUSH25 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makePushOp(25),
    ), 

    Opcode.PUSH25 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makePushOp(25),
    ), 
    
    Opcode.PUSH26 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makePushOp(26),
    ),

    Opcode.PUSH27 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makePushOp(27),
    ), 

    Opcode.PUSH28 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makePushOp(28),
    ), 
    
    Opcode.PUSH29 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makePushOp(29),
    ),  

    Opcode.PUSH30 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makePushOp(30),
    ), 
    
    Opcode.PUSH31 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makePushOp(31),
    ),

    Opcode.PUSH32 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makePushOp(32),
    ),

    Opcode.DUP1 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makeDupOp(1),
    ),

    Opcode.DUP2 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makeDupOp(2),
    ), 

    Opcode.DUP3 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makeDupOp(3),
    ), 

    Opcode.DUP4 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makeDupOp(4),
    ), 

    Opcode.DUP5 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makeDupOp(5),
    ), 

    Opcode.DUP6 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makeDupOp(6),
    ), 


    Opcode.DUP7 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makeDupOp(7),
    ), 

    Opcode.DUP8 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makeDupOp(8),
    ), 

    Opcode.DUP9 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makeDupOp(9),
    ), 

    Opcode.DUP10 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makeDupOp(10),
    ), 

    Opcode.DUP11 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makeDupOp(11),
    ), 

    Opcode.DUP12 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makeDupOp(12),
    ),

    Opcode.DUP13 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makeDupOp(13),
    ), 

    Opcode.DUP14 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makeDupOp(14),
    ), 

    Opcode.DUP15 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makeDupOp(15),
    ), 

    Opcode.DUP16 : EVMInstruction(
        immediate_value=True,
        immediate_size=1,
        gas_cost=0,
        execute=makeDupOp(16),
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

    Opcode.JUMPI : EVMInstruction(
        gas_cost=0,
        execute=opJumpI,
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

