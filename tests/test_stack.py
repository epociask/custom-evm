import vm.stack as stack


def test_stack_insert():
    s = stack.Stack()

    for num in range(0, 3, 1):
        s.push(num)
        print(s.stack)
    
    for num in range(2, -1, -1):
        assert s.pop() == num

def test_stack_invalid_word_size():
    s = stack.Stack()

    bit_500 = [0] * 100000

    try:
        s.push(bit_500)

    except stack.StackError as se:
        assert "Item size exceeds word size limit" in str(se)
        return

    assert False; "Exception not raised"

def test_empty_stack_exception():
    s = stack.Stack()

    try:
        s.pop()

    except stack.StackError as se:
        assert "Trying to read from empty stack" in str(se)
        return

    assert False; "Exception not raised"

def test_empty_stack_exception():
    s = stack.Stack()

    try:
        s.pop()

    except stack.StackError as se:
        assert "Trying to read from empty stack" in str(se)
        return

    assert 0 == 1

def test_max_stack_size_exception():
    s = stack.Stack(size=1024)

    for num in range(0, 1024, 1):
        s.push(num)

    try:
        s.push(2)

    except stack.StackError as se:
        assert "Maximum number of elements" in str(se)
        return

    assert False; "Exception not raised"