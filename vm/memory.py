import sys

"""
  YELLOW PAPER:
  * The memory model is a simple word-addressed byte array.

  Implementation inspiration taken directly from geth:
  - https://github.com/ethereum/go-ethereum/blob/b1e72f7ea998ad662166bcf23705ca59cf81e925/core/vm/memory.go
"""

## TODO: Actually represent memory as a word addressed byte array instead of byte key list

class Memory():
  store: list = []
  limit: int = 1000000

  def __init__(self):
    self.store = [None] * self.limit

  def set(self, offset: int, value: bytes):
    size = sys.getsizeof(value)

    if size > 0:
      if offset + size < self.limit:
        self.store[offset] = value

  def get(self, offset: int):
    return self.store[offset]