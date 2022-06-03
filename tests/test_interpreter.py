from vm.interpreter import EVMInterpreter
from vm.contract import Contract

def test_interpreter_add():
    with open("bytecodes/add.bytes") as f:
        hex_str = f.read()
    
    print(f"_{hex_str}_")
    result = bytearray.fromhex(hex_str)
    
    contract = Contract(result, None)
    interpreter = EVMInterpreter()
    interpreter.run(contract)

    assert interpreter.scope_ctx.stack.pop() == 192; "Ensuring resultant stack value is sum of 0x40 and 0x80"

def test_interpreter_arithmetic():
    with open("bytecodes/arithmetic.bytes") as f:
        hex_str = f.read()
    
    print(f"_{hex_str}_")
    result = bytearray.fromhex(hex_str)
    
    contract = Contract(result, None)
    interpreter = EVMInterpreter()
    interpreter.run(contract)

    assert interpreter.scope_ctx.stack.pop() == 0; "Ensuring resultant stack value is 0x00"