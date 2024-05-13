#: example6.py
# Multiple arguments in composition
# Using https://github.com/dry-python/returns
from returns.result import Failure, Result, Success, safe
from util import display
from validate_output import console


def func_a(i: int) -> Result[int, str]:
    if i == 1:
        return Failure(f"func_a({i})")
    return Success(i)


def func_b(i: int) -> Result[int, ZeroDivisionError]:
    if i == 0:
        return Failure(ZeroDivisionError(f"func_b({i})"))
    return Success(i)


@safe  # Convert existing function
def func_c(i: int) -> int:  # Result[int, ValueError]
    if i == 3:
        raise ValueError(f"func_c({i})")
    return i


# Pure function
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
    inputs := [(1, 5), (7, 0), (2, 1), (7, 5)],
    outputs=[composed(*args) for args in inputs],
)
console == """
(1, 5): <Failure: func_a(1)>
(7, 0): <Failure: func_b(0)>
(2, 1): <Failure: func_c(3)>
(7, 5): <Success: 24>
"""
