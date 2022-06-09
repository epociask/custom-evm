from vm.interpreter import EVMInterpreter
from vm.contract import Contract

import pytest

"""
NOTE: All test cases were written out by hand (opcode, bytecode) before validated against VM interpreter
"""

def test_interpreter_push_1():
    result = bytearray.fromhex("61 1111 00")
    
    contract = Contract(result, None)
    interpreter = EVMInterpreter()
    interpreter.run(contract)

    expected = 0x1111
    actual = interpreter.scope_ctx.stack.pop()

    assert expected == actual; "Ensuring resultant stack value is 2 bytes pushed 0x1111"

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

    expected_1, expected_2 = 0x010101011001100110010110, 0x11111111
    actual_1, actual_2 = interpreter.scope_ctx.stack.pop(), interpreter.scope_ctx.stack.pop()
    assert expected_1 == actual_1; "Ensuring 12 byte value is pushed on stack properly"
    assert expected_2 == actual_2; "Ensuring 4 byte value is pushed on stack properly"

def test_interpreter_add():
    result = bytearray.fromhex("6080 6040 01")
    
    contract = Contract(result, None)
    interpreter = EVMInterpreter()
    interpreter.run(contract)

    expected = 192
    actual = interpreter.scope_ctx.stack.pop()

    assert expected == actual; "Ensuring resultant stack value is sum of 0x40 and 0x80"

def test_interpreter_arithmetic():
    result = bytearray.fromhex("6001 6001 01 6002 03")
    
    contract = Contract(result, None)
    interpreter = EVMInterpreter()
    interpreter.run(contract)

    expected = 0x0
    actual = interpreter.scope_ctx.stack.pop()

    assert expected == actual; "Ensuring resultant stack value is 0x00"

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

    expected = 0x04
    actual = interpreter.scope_ctx.stack.pop()

    assert expected == actual; "Ensuring resultant stack value is 0x04"

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

    expected = (1/2)
    actual = interpreter.scope_ctx.stack.pop()

    assert expected == actual; "Ensuring resultant stack value is (1/2)"
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

@pytest.mark.parametrize("opcode,expected", [
    ("16", 0b00000000), # AND
    ("17", 0b11110000), # OR
    ("18", 0b11110000),  # XOR
    ("19", 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff5f), # NOT
    ])
def test_bitwise(opcode, expected):
    """
    ASSEMBLY VIEW:
    #0 PUSH1 0x50
    #2 PUSH1 0xA0
    #4 OPERATION 
    #5 STOP
    """
    result = bytearray.fromhex(f"6050 60A0 {opcode} 00")

    contract = Contract(result, None)
    interpreter = EVMInterpreter()
    interpreter.run(contract)

    assert interpreter.scope_ctx.stack.pop() == expected; f"Ensuring resultant stack value is {expected}"

@pytest.mark.parametrize("bytecode,expected", [
    ## LSL ## 
    ("60FF 6002 1B 00", 0x3FC), # PUSH1 0xFF #PUSH1 0x02 #SHL #STOP 
    ("7F9d10a14bbcf24a02577408aadba99177cd90328457cb54f402384c7f0fe45e3860021B00", 0x7442852ef3c928095dd022ab6ea645df3640ca115f2d53d008e131fc3f9178e0), #PUSH32 VAL #PUSH1 0x02 #SHL #STOP
    ("7F 9d10a14bbcf24a02577408aadba99177cd90328457cb54f402384c7f0fe45e38 7F FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF 1B 00", 0x0), #PUSH32 VAL #PUSH32 MAX #SHL STOP

    ## SAR ##
    ("60FF 6002 1D", 0x3F), #PUSH1 0xFF #PUSH1 0x02 #SAR #STOP
    ("7F9d10a14bbcf24a02577408aadba99177cd90328457cb54f402384c7f0fe45e3860021D00", 0xe7442852ef3c928095dd022ab6ea645df3640ca115f2d53d008e131fc3f9178e), #PUSH32 VAL #PUSH1 0x02 #SAR #STOP
    # ("7F 9d10a14bbcf24a02577408aadba99177cd90328457cb54f402384c7f0fe45e38 7F FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF 1D 00", 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff), #PUSH32 VAL #PUSH32 MAX #SHL STOP
   

    ## SHR ##
    ("60FF 6002 1C", 0x3F),
    ("7F9d10a14bbcf24a02577408aadba99177cd90328457cb54f402384c7f0fe45e3860021C00", 0x27442852ef3c928095dd022ab6ea645df3640ca115f2d53d008e131fc3f9178e)

    ## BYTE ##

    

 ])
def test_shifts(bytecode, expected):
    """
    ASSEMBLY VIEW:
    #0 PUSH1 0x02
    #2 PUSH1 0xA0
    #4 OPERATION 
    #5 STOP
    """
    result = bytearray.fromhex(bytecode)

    contract = Contract(result, None)
    interpreter = EVMInterpreter()
    interpreter.run(contract)

    actual = interpreter.scope_ctx.stack.pop()

    assert actual == expected; f"Ensuring resultant stack value is {expected}"

@pytest.mark.parametrize("bytecode,expected_stack", [
    ("6001 80 00", [1,1]), # DUP1
    ("6001 6002 81 00", [1,2,1]), # DUP2
    ("6001 6002 6003 82 00", [1,3,2,1]), # DUP3
    ("6001 6002 6003 6004 83 00", [1,4,3,2,1]), # DUP4
    ("6001 6002 6003 6004 6005 84 00", [1,5,4,3,2,1]), # DUP5
    ("6001 6002 6003 6004 6005 6006 85 00", [1,6,5,4,3,2,1]), # DUP6
    ("6001 6002 6003 6004 6005 6006 6007 86 00", [1,7,6,5,4,3,2,1]), # DUP7
    ("6001 6002 6003 6004 6005 6006 6007 6008 87 00", [1,8,7,6,5,4,3,2,1]), # DUP8
    ("6001 6002 6003 6004 6005 6006 6007 6008 6009 88 00", [1,9,8,7,6,5,4,3,2,1]), # DUP9
    ("6001 6002 6003 6004 6005 6006 6007 6008 6009 600A 89 00", [1,10,9,8,7,6,5,4,3,2,1]), # DUP10
    ("6001 6002 6003 6004 6005 6006 6007 6008 6009 600A 600B 8A 00", [1,11,10,9,8,7,6,5,4,3,2,1]), # DUP11
    ("6001 6002 6003 6004 6005 6006 6007 6008 6009 600A 600B 600C 8B 00", [1,12,11,10,9,8,7,6,5,4,3,2,1]), # DUP12
    ("6001 6002 6003 6004 6005 6006 6007 6008 6009 600A 600B 600C 600D 8C 00", [1,13,12,11,10,9,8,7,6,5,4,3,2,1]), # DUP13
    ("6001 6002 6003 6004 6005 6006 6007 6008 6009 600A 600B 600C 600D 600E 8D 00", [1,14,13,12,11,10,9,8,7,6,5,4,3,2,1]), # DUP14
    ("6001 6002 6003 6004 6005 6006 6007 6008 6009 600A 600B 600C 600D 600E 600F 8E 00", [1,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1]), # DUP15
    ("6001 6002 6003 6004 6005 6006 6007 6008 6009 600A 600B 600C 600D 600E 600F 6010 8F 00", [1,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1]), # DUP16
    ])
def test_dups(bytecode, expected_stack: list):
    """
    ASSEMBLY VIEW:
    #0 PUSH1 0x02
    #2 PUSH1 0xA0
    #4 OPERATION 
    #5 STOP
    """
    result = bytearray.fromhex(bytecode)

    contract = Contract(result, None)
    interpreter = EVMInterpreter()
    interpreter.run(contract)

    print("Actual stack", interpreter.scope_ctx.stack.stack)
    print("Expected stack", expected_stack)
    while interpreter.scope_ctx.stack.count != 0:
        expected = expected_stack.pop(0)
        actual = interpreter.scope_ctx.stack.pop()

        assert expected == actual
    
    interpreter.scope_ctx.stack.reset()

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

    expected = 0x0C
    actual = interpreter.scope_ctx.stack.pop()

    assert expected == actual

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

    expected = 0x06
    actual = interpreter.scope_ctx.stack.pop()

    assert expected == actual

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

    expected = 0x08
    actual = interpreter.scope_ctx.stack.pop()

    assert expected == actual

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

    expected = 0x09
    actual = interpreter.scope_ctx.stack.pop()

    assert  expected == actual

@pytest.mark.parametrize("bytecode,expected", [
    # GT (0x11) #
    ("6002 6001 11 00", 0),
    ("6001 6002 11 00", 1),

    # SGT (0x13) #

    # # EQ (0x14) #
    ("6012 6012 14 00", 1),
    ("6012 6011 14 00", 0),

    # # LT (0x10) #
    ("6002 6001 11 00", 0),
    ("6001 6002 11 00", 1),

    # SLT (0x12) #

    # ISZERO (0x15) #
    ("6000 15 00", 1),
    ("6001 15 00", 0)
    ])
def test_conditionals(bytecode, expected):
    result = bytearray.fromhex(bytecode)

    contract = Contract(result, None)
    interpreter = EVMInterpreter()
    interpreter.run(contract)

    actual = interpreter.scope_ctx.stack.pop()
    assert  expected == actual