from dataclasses import dataclass
from importlib.resources import open_text
from vm.interpreter import EVMInterpreter
from vm.contract import Contract

"""
NOTE: All test cases were written out by hand (opcode, bytecode) before validated against VM interpreter
"""

def test_interpreter_push_1():
    result = bytearray.fromhex("61 1111 00")
    
    contract = Contract(result, None)
    interpreter = EVMInterpreter()
    interpreter.run(contract)

    assert interpreter.scope_ctx.stack.pop() == 0x1111; "Ensuring resultant stack value is 2 bytes pushed 0x1111"

def test_interpreter_push_2():
    """
    ASSEMBLY VIEW:
    #0  PUSH4 0x11111111
    #6  PUSH12 0x010101011001100110010110
    #20 STOP
    """
    result = bytearray.fromhex("63 11111111 6B 010101011001100110010110 00")
    
    contract = Contract(result, None)
    interpreter = EVMInterpreter()
    interpreter.run(contract)

    assert interpreter.scope_ctx.stack.pop() == 0x010101011001100110010110; "Ensuring 12 byte value is pushed on stack properly"
    assert interpreter.scope_ctx.stack.pop() == 0x11111111; "Ensuring 4 byte value is pushed on stack properly"

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

def test_bitwise():
    """
    ASSEMBLY VIEW:
    #0 PUSH1 0x50
    #2 PUSH1 0xA0
    #4 OPERATION 
    #5 STOP
    """
    # AND, OR, XOR#
    op_tests = [
        {"opcode": "16", "expected": 0b00000000},
        {"opcode": "17", "expected": 0b11110000},
        {"opcode": "18", "expected": 0b11110000},
        ]

    for test in op_tests:
        op = test["opcode"]
        result = bytearray.fromhex(f"6050 60A0 {op} 00")
    
        contract = Contract(result, None)
        interpreter = EVMInterpreter()
        interpreter.run(contract)

        expected = test["expected"]
        assert interpreter.scope_ctx.stack.pop() == expected; f"Ensuring resultant stack value is {expected}"

def test_shifts():
    """
    ASSEMBLY VIEW:
    #0 PUSH1 0x02
    #2 PUSH1 0xA0
    #4 OPERATION 
    #5 STOP
    """
    # SHL, SHR, SAR#
    op_tests = [
        # PUSH1 0x02 #PUSH1 0xFF #SHL #STOP 
        {"bytecode": "60FF 6002 1B 00", "expected": 0b11111100},

        # {"opcode": "1C", "expected": 0b11110000},
        # {"opcode": "1D", "expected": 0b11110000},
        ]

    for test in op_tests:
        instructions = test["bytecode"]
        result = bytearray.fromhex(instructions)
    
        contract = Contract(result, None)
        interpreter = EVMInterpreter()
        interpreter.run(contract)

        expected = test["expected"]
        assert interpreter.scope_ctx.stack.pop() == expected; f"Ensuring resultant stack value is {expected}"



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

def test_jump_conditional_0():
    """
    ASSEMBLY VIEW:
    #0  PUSH1 0x04
    #2  PUSH1 0x04
    #4  EQ
    #5  PUSH1 0x0B
    #7  JUMPI
    #8  PUSH1 0x09
    #10 STOP
    #11 JUMPDEST
    #12 PUSH1 0x08
    #14 STOP
    """
    result = bytearray.fromhex("6004 6004 14 600B 57 60 09 00 5B 60 08 00")
    
    contract = Contract(result, None)
    interpreter = EVMInterpreter()
    interpreter.run(contract)

    assert interpreter.scope_ctx.stack.pop() == 0x08; "Ensuring resultant stack value is 0x08"

def test_jump_conditional_1():
    """
    ASSEMBLY VIEW: 
    #0  PUSH1 0x04
    #2  PUSH1 0x03
    #4  EQ
    #5  PUSH1 0x0B
    #7  JUMPI
    #8  PUSH1 0x09
    #10 STOP
    #11 JUMPDEST
    #12 PUSH1 0x08
    #14 STOP
    """
    result = bytearray.fromhex("6004 6003 14 600B 57 60 09 00 5B 60 08 00")
    
    contract = Contract(result, None)
    interpreter = EVMInterpreter()
    interpreter.run(contract)

    assert interpreter.scope_ctx.stack.pop() == 0x09; "Ensuring resultant stack value is 0x08"
