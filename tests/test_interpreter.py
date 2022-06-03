from dataclasses import dataclass
from vm.interpreter import EVMInterpreter
from vm.contract import Contract

"""
NOTE: All test cases were written out by hand (opcode, bytecode) before validated against VM interpreter
"""

## TODO: Modularize tests
#@dataclass
#class TestCase:
#    file_dir: str
#    _input: str
#    assertions: object

def test_interpreter_add():
    result = bytearray.fromhex("6080 6040 01")
    
    contract = Contract(result, None)
    interpreter = EVMInterpreter()
    interpreter.run(contract)

    assert interpreter.scope_ctx.stack.pop() == 192; "Ensuring resultant stack value is sum of 0x40 and 0x80"

def test_interpreter_arithmetic():
    result = bytearray.fromhex("6001 6001 01 6002 03")
    
    contract = Contract(result, None)
    interpreter = EVMInterpreter()
    interpreter.run(contract)

    assert interpreter.scope_ctx.stack.pop() == 0; "Ensuring resultant stack value is 0x00"

def test_interpreter_arithmetic_1():
    """
    ASSEMBLY VIEW:
        #0 PUSH1 0x05
        #2 PUSH1 0x04
        #4 PUSH1 0x05
        #5 MUL
        #6 DIV
        #7 STOP
    """
    result = bytearray.fromhex("6005 6004 6005 02 04 00")
    
    contract = Contract(result, None)
    interpreter = EVMInterpreter()
    interpreter.run(contract)

    assert interpreter.scope_ctx.stack.pop() == 4; "Ensuring resultant stack value is 0x04"

def test_interpreter_arithmetic_2():
    """
    ASSEMBLY VIEW:
        #0  PUSH1 0x02
        #2  PUSH1 0x03
        #4  PUSH1 0x04
        #6  PUSH1 0x06
        #8  PUSH1 0x02
        #10 PUSH1 0x03
        #12 PUSH1 0x02
        #14 ADDMOD
        #15 EXP
        #16 MULMOD
        #18 STOP
    """
    #NOTE: ADDMOD(2,3,2) -> EXP (x, 6) -> MULMOD(x,4,3) -> DIV(x,2) = 1/2
    result = bytearray.fromhex("6002 6003 6004 6006 6002 6003 6002 08 0A 09 04 00")
    
    contract = Contract(result, None)
    interpreter = EVMInterpreter()
    interpreter.run(contract)

    assert interpreter.scope_ctx.stack.pop() == (1/2); "Ensuring resultant stack value is (1/2)"

def test_jump_0():
    """
    ASSEMBLY VIEW:
        #0 PUSH1 0x03
        #2 PUSH1 0x04
        #4 PUSH1 0x08
        #6 JUMP
        #7 ADD
        #8 JUMPDEST
        #9 MUL
        #10 STOP
    """
    result = bytearray.fromhex("6003 6004 6008 56 01 5b 02 00")
    
    contract = Contract(result, None)
    interpreter = EVMInterpreter()
    interpreter.run(contract)

    assert interpreter.scope_ctx.stack.pop() == 12; "Ensuring resultant stack value is product of (4*3)"

def test_jump_1():
    """
    ASSEMBLY VIEW:
        #0 PUSH1 0x0C
        #2 JUMP
        #3 PUSH1 0x04
        #5 PUSH1 0x08
        #7 JUMPDEST
        #8 PUSH1 0x04
        #10 ADD
        #11 STOP
        #12 JUMPDEST
        #13 PUSH1 0x02
        #15 PUSH1 0x07
        #17 JUMP
    """
    result = bytearray.fromhex("600C 56 6004 6008 5B 6004 01 00 5B 6002 6007 56")
    
    contract = Contract(result, None)
    interpreter = EVMInterpreter()
    interpreter.run(contract)

    assert interpreter.scope_ctx.stack.pop() == 6; "Ensuring resultant stack value is 4+2"

