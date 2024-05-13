#: example6.py
# Multiple arguments in composition
from example4 import func_a, func_b, func_c
from returns.result import Result
from util import display
from validate_output import console


def add(first: int, second: int, third: int) -> int:
    return first + second + third


def composed(
    i: int, j: int
) -> Result[int, str | ZeroDivisionError | ValueError]:
    # fmt: off
    return Result.do(
        add(first, second, third)
        for first in func_a(i)
        for second in func_b(j)
        for third in func_c(i + j)
    )


display(
    inputs := [(1, 5), (7, 2), (2, 1), (7, 5)],
    outputs=[composed(*args) for args in inputs],
)
console == """
(1, 5): <Failure: func_a(1)>
(7, 2): <Failure: func_b(2)>
(2, 1): <Failure: func_c(3): division by zero>
(7, 5): <Success: 24>
"""
