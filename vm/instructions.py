from dataclasses import dataclass
import numpy
import sha3
import sys

from vm.opcode import Opcode
from vm.pc import ProgramCounter
from vm.machine_ctx import  MachineContext
from vm.constants import (
    MAX_UINT_256,
    MAX_256_HEX,
    BIG_ENDIAN,
    )

"""
Instruction logic taken from pseudocode presented in:
    * https://www.ethervm.io/ 
    * https://ethereum.org/en/developers/docs/evm/opcodes/
"""

bool_to_bin = lambda b: 0 if b is False else 1


##                                   ##
#   Instruction defintion functions   #
##                                   ##
def opAdd(pc: ProgramCounter, interp, ctx: MachineContext):
    x, y = ctx.stack.pop(), ctx.stack.pop()
    z: int = (x + y) & MAX_UINT_256

    ctx.stack.push(z)

def opSub(pc: ProgramCounter, interp, ctx: MachineContext):
    x, y = ctx.stack.pop(), ctx.stack.pop()
    z: int = (x - y) & MAX_UINT_256

    ctx.stack.push(z)

def opMul(pc: ProgramCounter, interp, ctx: MachineContext):
    x, y = ctx.stack.pop(), ctx.stack.pop()
    z: int = (x * y) & MAX_UINT_256

    ctx.stack.push(z)

def opDiv(pc: ProgramCounter, interp, ctx: MachineContext):
    # TODO: test more thoroughly 
    # TODO: Edge case /// divide by zero?
    x, y = ctx.stack.pop(), ctx.stack.pop()
    z = x / y

    ctx.stack.push(z)

def opMod(pc: ProgramCounter, interp, ctx: MachineContext):
    x, y = ctx.stack.pop(), ctx.stack.pop()
    z: int = x % y

    ctx.stack.push(z)

def opAddMod(pc: ProgramCounter, interp, ctx: MachineContext):
    x, y, n = ctx.stack.pop(), ctx.stack.pop(), ctx.stack.pop()
    z: int = (x+y) % n
    ctx.stack.push(z)

def opMulMod(pc: ProgramCounter, interp, ctx: MachineContext):
    x, y, n = ctx.stack.pop(), ctx.stack.pop(), ctx.stack.pop()
    z: int = (x*y) % n
    ctx.stack.push(z)

def opExp(pc: ProgramCounter, interp, ctx: MachineContext):
    x, y = ctx.stack.pop(), ctx.stack.pop()
    z: int = x ** y

    ctx.stack.push(z)

def opJump(pc: ProgramCounter, interp, ctx: MachineContext):
    dest = ctx.stack.pop()
    print("Jumping to ", dest)
    pc.set(dest)

def opJumpDest(pc: ProgramCounter, interp, ctx: MachineContext):
    pass

def opJumpI(pc: ProgramCounter, interp, ctx: MachineContext):
    dest, cond = ctx.stack.pop(), ctx.stack.pop()

    if cond:
        pc.set(dest)


def opLt(pc: ProgramCounter, interp, ctx: MachineContext):
    a, b = ctx.stack.pop(), ctx.stack.pop()
    c: bin = bool_to_bin((a < b))

    ctx.stack.push(c)

def opSgt(pc: ProgramCounter, interp, ctx: MachineContext):
    # TODO: implement 
    pass

def opSlt(pc: ProgramCounter, interp, ctx: MachineContext):
    # TODO: implement 
    pass

def opGt(pc: ProgramCounter, interp, ctx: MachineContext):
    a, b = ctx.stack.pop(), ctx.stack.pop()
    c: int = bool_to_bin((a > b))

    ctx.stack.push(c)

def opEq(pc: ProgramCounter, interp, ctx: MachineContext):
    a, b = ctx.stack.pop(), ctx.stack.pop()
    c: int = bool_to_bin((a == b))

    ctx.stack.push(c)

def opIsZero(pc: ProgramCounter, interp, ctx: MachineContext):
    a = ctx.stack.pop()
    c: int = bool_to_bin((a == 0))

    ctx.stack.push(c)

def opAnd(pc: ProgramCounter, interp, ctx: MachineContext):
    a, b = ctx.stack.pop(), ctx.stack.pop()
    c: bin = (a & b) #bitwise and

    ctx.stack.push(c)

def opOr(pc: ProgramCounter, interp, ctx: MachineContext):
    a, b = ctx.stack.pop(), ctx.stack.pop()
    c: bin = (a | b) #bitwise or

    ctx.stack.push(c)

def opXor(pc: ProgramCounter, interp, ctx: MachineContext):
    a, b = ctx.stack.pop(), ctx.stack.pop()
    c: bin = (a ^ b)

    ctx.stack.push(c)

def opNot(pc: ProgramCounter, interp, ctx: MachineContext):
    a = ctx.stack.pop()
    c: int = MAX_UINT_256 - a
    
    ctx.stack.push(c)

def opByte(pc: ProgramCounter, interp, ctx: MachineContext):
    #TODO: Test me
    i, x = ctx.stack.pop(), ctx.stack.pop()
    y = (x >> (248 - i * 8)) & 0xFF

    ctx.stack.push(y)

def opShl(pc: ProgramCounter, interp, ctx: MachineContext):
    shift, value = ctx.stack.pop(), ctx.stack.pop()
    
    if shift == MAX_256_HEX:
        result = 0
    else:
        result = numpy.left_shift(value, shift) & MAX_UINT_256

    ctx.stack.push(result)

def opShr(pc: ProgramCounter, interp, ctx: MachineContext):
    shift, value = ctx.stack.pop(), ctx.stack.pop()

    if shift == MAX_256_HEX:
        result = 0
    
    else:
        result = numpy.right_shift(value, shift) & MAX_UINT_256
    
    ctx.stack.push(result)

def opSar(pc: ProgramCounter, interp, ctx: MachineContext):
    shift, value = ctx.stack.pop(), ctx.stack.pop()
    
    shifted_value = value >> shift
    result = shifted_value & MAX_256_HEX
    ctx.stack.push(result)

def opSha3(pc: ProgramCounter, interp, ctx: MachineContext):
    #TODO: Test me
    offset = ctx.stack.pop()
    value = ctx.mem.get(offset)

    hasher = sha3.keccak_256()
    hasher.update(value)
    
    ctx.push(hasher.hexidigest())

def opMload(pc: ProgramCounter, interp, ctx: MachineContext):
    #TODO: Test me
    offset = ctx.stack.pop()
    val = ctx.mem.get(offset)

    ctx.stack.push(val)

def opMstore(pc: ProgramCounter, interp, ctx: MachineContext):
    #TODO: Test me
    value, offset = ctx.stack.pop(), ctx.stack.pop()

    ctx.mem.store(offset, value)

def opCallValue(pc: ProgramCounter, interp, ctx: MachineContext):
    call_value: int = ctx.contract.value & MAX_UINT_256

    ctx.stack.push(call_value)

def opCodeSize(pc: ProgramCounter, interp, ctx: MachineContext):
    size: int = len(ctx.contract.code)

    ctx.stack.push(size)

def opCallDataSize(pc: ProgramCounter, interp, ctx: MachineContext):
    size: int = sys.getsizeof(ctx.contract.data)

    ctx.stack.push(size)

def opCallDataLoad(pc: ProgramCounter, interp, ctx: MachineContext):
    first_32_bytes = ctx.contract.code[0 : 32]
    value = int.from_bytes(first_32_bytes, byteorder=BIG_ENDIAN)

    ctx.stack.push(value)

def makePushOp(offset_bytes: int):
    def pushN(pc: ProgramCounter, interp, ctx: MachineContext):
        pc.increment()
        byte_val = ctx.contract.code[pc.get() : pc.get() + offset_bytes]
        int_val = int.from_bytes(byte_val, BIG_ENDIAN) #Big Endian ordering 
        
        pc.increment(offset_bytes-1)
        ctx.stack.push(int_val)


    return pushN

def makeDupOp(position: int):
    def dupN(pc: ProgramCounter, interp, ctx: MachineContext):
        ctx.stack.duplicate(position-1)

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
    ),

    Opcode.CALLVALUE : EVMInstruction(
        gas_cost=0,
        execute=opCallValue,
    ),

    Opcode.CODESIZE : EVMInstruction(
        gas_cost=0,
        execute=opCodeSize,
    ),

    Opcode.CALLDATASIZE : EVMInstruction(
        gas_cost=0,
        execute=opCallDataSize,
    ),

    Opcode.CALLDATALOAD : EVMInstruction(
        gas_cost=0,
        execute=opCallDataLoad,
    )
}

