from vm.memory import Memory

def test_memory():
    mem = Memory()
    test_vals = [[0, 1, 0b10101], [4356, 4, 0b10101001010010101100101010], [5, 1, 0b10101010]]

    for val in test_vals:
        mem.set(val[0], val[1], val[2])

    for val in test_vals:
        mem_val = mem.get(val[0], val[1])

        assert mem_val == val[2]