#: comprehension4.py
# Composing functions
from comprehension3 import func_a
from result import Failure, Result, Success
from util import display
from validate_output import console


# Use an exception as info (but don't raise it):
def func_b(i: int) -> Result[int, ZeroDivisionError]:
    if i == 0:
        return Failure(ZeroDivisionError(f"func_b({i})"))
    return Success(i)


def func_c(i: int) -> Result[str, ValueError]:
    if i == -1:
        return Failure(ValueError(f"func_c({i})"))
    return Success(f"func_c({i})")


def composed(
    i: int,
) -> Result[str, str | ZeroDivisionError | ValueError]:
    result_a = func_a(i)
    if isinstance(result_a, Failure):
        return result_a

    result_b = func_b(
        result_a.unwrap()  # unwrap gets the value from Ok
    )
    if isinstance(result_b, Failure):
        return result_b

    return func_c(result_b.unwrap())


if __name__ == "__main__":
    display(
        inputs := range(-1, 3),
        outputs := [composed(i) for i in inputs],
    )
    console == """
-1: Failure(error=ValueError('func_c(-1)'))
0: Failure(error=ZeroDivisionError('func_b(0)'))
1: Failure(error='func_a(1)')
2: Success(value='func_c(2)')
"""
