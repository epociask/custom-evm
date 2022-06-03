from dataclasses import dataclass
from vm.interpreter import EVMInterpreter
from vm.contract import Contract


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
    result = bytearray.fromhex("6005 6004 6005 02 04")
    
    contract = Contract(result, None)
    interpreter = EVMInterpreter()
    interpreter.run(contract)

    assert interpreter.scope_ctx.stack.pop() == 4; "Ensuring resultant stack value is 0x04"

def test_interpreter_arithmetic_2():
    #NOTE: ADDMOD(2,3,2) -> EXP (x, 6) -> MULMOD(x,4,3) -> DIV(x,2) = 1/2
    result = bytearray.fromhex("6002 6003 6004 6006 6002 6003 6002 08 0A 09 04")
    
    contract = Contract(result, None)
    interpreter = EVMInterpreter()
    interpreter.run(contract)

    assert interpreter.scope_ctx.stack.pop() == (1/2); "Ensuring resultant stack value is (1/2)"