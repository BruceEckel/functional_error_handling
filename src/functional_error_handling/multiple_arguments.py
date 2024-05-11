#: multiple_arguments.py
from comprehension6 import func_a, func_b
from returns.result import Result
from util import display
from validate_output import console


def add(first: int, second: int) -> int:
    return first + second


def composed(i: int, j: int) -> Result[int, str | ValueError]:
    # fmt: off
    return Result.do(
        add(first, second)
        for first in func_a(i)
        for second in func_b(j)
    )


inputs = [(1, 5), (7, 0), (2, 1)]
outputs = [composed(*args) for args in inputs]
display(inputs, outputs)
console == """
(1, 5): <Failure: func_a(i = 1)>
(7, 0): <Failure: func_b(i =0)>
(2, 1): <Success: 3>
"""
