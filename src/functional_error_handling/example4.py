#: example4.py
# Composing functions
from returns.result import Failure, Result, Success
from util import display
from validate_output import console


def func_a(i: int) -> Result[int, str]:
    if i == 1:
        return Failure(f"func_a({i})")
    return Success(i)


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
        result_a.unwrap()  # unwrap gets the answer from Success
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
-1: <Failure: func_c(-1)>
0: <Failure: func_b(0)>
1: <Failure: func_a(1)>
2: <Success: func_c(2)>
"""
