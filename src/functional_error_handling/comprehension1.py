# import pretty_errors


def f1(i: int) -> int:
    if i == 5:
        raise ValueError("i cannot be 5")
    else:
        return i * 2


print([f1(i) for i in range(10)])
