from dataclasses import dataclass

from vm.memory import Memory
from vm.stack import Stack
from vm.contract import Contract

@dataclass
class MachineContext:
    contract: Contract
    mem: Memory
    stack: Stack 
