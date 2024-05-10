#: multiple_arguments.py
from returns.result import Failure, Result, Success
from util import display
from validate_output import console


def reject_1(i: int) -> Result[int, ValueError]:
    if i == 1:
        return Failure(ValueError(f"reject_1: {i = }"))
    return Success(i * 10)


def reject_2(j: int) -> Result[int, ValueError]:
    if j == 2:
        return Failure(ValueError(f"reject_2: {j = }"))
    return Success(j * 100)


# Ordinary function:
def add(first: int, second: int) -> int:
    return first + second


def composed(i: int, j: int) -> Result[int, ValueError]:
    # fmt: off
    return Result.do(
        add(first, second)
        for first in reject_1(i)
        for second in reject_2(j)
    )


inputs = [(1, 5), (7, 2), (2, 1)]
outputs = [composed(*args) for args in inputs]
display(inputs, outputs)
console == """
(1, 5): <Failure: reject_1: i = 1>
(7, 2): <Failure: reject_2: j = 2>
(2, 1): <Success: 120>
"""
