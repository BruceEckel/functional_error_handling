#: multiple_arguments_io_do.py
from returns.io import IO


def add(first: int, second: int) -> int:
    return first + second


def do_add(i: int, j: int) -> int:
    # fmt: off
    return IO.do(
        add(first, second) 
        for first in IO(i) 
        for second in IO(j)
    )


print(do_add(1, 2))  # <IO: 3>
