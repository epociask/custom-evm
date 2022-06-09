from dataclasses import dataclass

from vm.memory import Memory
from vm.stack import Stack

@dataclass
class MachineContext:
    code: list
    mem: Memory
    stack: Stack 
