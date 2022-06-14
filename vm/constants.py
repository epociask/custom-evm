from enum import IntEnum, unique
from dataclasses import dataclass

BIG_ENDIAN = "big"
LITTLE_ENDIAN = "little"

MAX_UINT_256: int = (2**256)-1
MAX_256_HEX: hex = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF

@unique
class ReturnCode(IntEnum):
    STOPPED = 0x0
    REVERTED = 0x1

@dataclass
class CompletedExecution:
    code: ReturnCode
    data: bytearray
