#: example4.py
# Composing functions
# Using https://github.com/dry-python/returns
from example3 import func_a
from returns.result import Failure, Result, Success, safe
from util import display
from validate_output import console


# Use an exception as info (but don't raise it):
def func_b(i: int) -> Result[int, ValueError]:
    if i == 2:
        return Failure(ValueError(f"func_b({i})"))
    return Success(i)


# Convert exception to Failure:
def func_c(i: int) -> Result[int, ZeroDivisionError]:
    try:
        1 / (i - 3)
    except ZeroDivisionError as e:
        return Failure(
            ZeroDivisionError(f"func_c({i}): {e}")
        )
    return Success(i)


@safe  # Convert existing function
def func_d(i: int) -> str:  # Result[str, ZeroDivisionError]
    1 / i
    return f"func_d({i})"


def composed(
    i: int,
) -> Result[str, str | ValueError | ZeroDivisionError]:
    result_a = func_a(i)
    if isinstance(result_a, Failure):
        return result_a

    # unwrap() gets the answer from Success:
    result_b = func_b(result_a.unwrap())
    if isinstance(result_b, Failure):
        return result_b

    result_c = func_c(result_b.unwrap())
    if isinstance(result_c, Failure):
        return result_c

    return func_d(result_c.unwrap())


if __name__ == "__main__":
    display(
        inputs := range(5),
        outputs := [composed(i) for i in inputs],
    )
    console == """
0: <Failure: division by zero>
1: <Failure: func_a(1)>
2: <Failure: func_b(2)>
3: <Failure: func_c(3): division by zero>
4: <Success: func_d(4)>
"""
