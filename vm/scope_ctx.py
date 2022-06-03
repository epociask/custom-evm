from dataclasses import dataclass

from vm.memory import Memory
from vm.stack import Stack

@dataclass
class ScopeContext:
    code: list
    mem: Memory
    stack: Stack 
