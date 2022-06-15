from vm.opcode import Opcode
from vm.instructions import ReferenceTable

def main():
    ops = [e for e in Opcode]
    unimplemented = []

    for op in ops:
        if op not in ReferenceTable:
            unimplemented.append(op)

    print(unimplemented)

if __name__ == "__main__":
    main()
