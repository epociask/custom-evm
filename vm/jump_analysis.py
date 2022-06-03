"""
We previously used "D" as the function to determine the set of valid jump destinations given the code that is being run. We define this
as any position in the code occupied by a JUMPDEST
instruction.
All such positions must be on valid instruction boundaries, rather than sitting in the data portion of PUSH
operations and must appear within the explicitly defined
portion of the code (rather than in the implicitly defined
STOP operations that trail it).
"""


def gen_jump_map(code: bytes)->dict:
