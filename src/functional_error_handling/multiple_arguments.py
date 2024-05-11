#: multiple_arguments.py
from returns.result import Failure, Result, Success
from util import display
from validate_output import console


def func_a(i: int) -> Result[int, ValueError]:
    if i == 1:
        return Failure(ValueError(f"func_a: {i = }"))
    return Success(i * 10)


def func_b(j: int) -> Result[int, ValueError]:
    if j == 2:
        return Failure(ValueError(f"func_b: {j = }"))
    return Success(j * 100)


# Ordinary function:
def add(first: int, second: int) -> int:
    return first + second


def composed(i: int, j: int) -> Result[int, ValueError]:
    # fmt: off
    return Result.do(
        add(first, second)
        for first in func_a(i)
        for second in func_b(j)
    )


inputs = [(1, 5), (7, 2), (2, 1)]
outputs = [composed(*args) for args in inputs]
display(inputs, outputs)
console == """
(1, 5): <Failure: func_a: i = 1>
(7, 2): <Failure: func_b: j = 2>
(2, 1): <Success: 120>
"""
