#: multiple_arguments.py
from returns.result import Failure, Result, Success
from util import display
from validate_output import console


def reject_1(i: int) -> Result[int, ValueError]:
    if i == 1:
        return Failure(ValueError(f"not_one: {i = }"))
    return Success(i * 10)


def reject_2(j: int) -> Result[int, ValueError]:
    if j == 2:
        return Failure(ValueError(f"not_two: {j = }"))
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


inputs = [(1, 5), (7, 2), (3, 4)]
outputs = [composed(*args) for args in inputs]
display(inputs, outputs)
console == """
(1, 5): <Failure: not_one: i = 1>
(7, 2): <Failure: not_two: j = 2>
(3, 4): <Success: 430>
"""
