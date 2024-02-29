def f1(i: int) -> int:
    if i == 3:
        raise ValueError("i cannot be 3")
    else:
        return i * 2


print([f1(i) for i in range(5)])
