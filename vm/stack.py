import sys


"""
Yellowpaper requirements:
  * The word size of the machine is 256-bit.
  * The stack has a maximum size of 1024.
"""
class StackError(Exception):
    pass


class Stack():
    stack: list = []
    count: int = 0

    def __init__(self, size: int=1024):
        self.size = size

    def __str__(self) -> str:
        return str(self.stack)
    
    def reset(self):
        self.stack = []
        self.count = 0
        
    def push(self, item: bytes):
        if sys.getsizeof(item) > 256:
            raise StackError("Item size exceeds word size limit (256 bits)")

        if self.count == self.size:
            raise StackError(f"Maximum number of elements ({self.size}) exceeded")
        
        self.stack.insert(0, item)
        self.count += 1
    
    def duplicate(self, position: int):
        self.push(self.stack[position])

    def pop(self) -> bytes:
        if self.count == 0:
            raise StackError("Trying to read from empty stack")
        
        self.count -= 1
        return self.stack.pop(0)

    def peak(self) -> bytes:
        if self.count == 0:
            raise StackError("Trying to read from empty stack")
        
        return self.stack[0]