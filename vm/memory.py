"""
  * The memory model is a simple word-addressed byte array. 
"""

class Memory():
  store: list = []
  limit: int = 1000000

  def set(self, offset: int, value: bytes):
    size = len(value)

    if size > 0:
      if offset + size > self.limit:
        self.store[offset] = value

  def get(self, offset: int):
    return self.storage[offset]