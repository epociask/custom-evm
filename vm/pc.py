from dataclasses import dataclass

@dataclass
class ProgramCounter:
    pc: int

    def increment(self, amount: int=1):
        self.pc+=amount

    def get(self):
        return self.pc