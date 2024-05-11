#: comprehension4.py
# Composing functions
from comprehension3 import func_a
from result import Err, Ok, Result
from util import display
from validate_output import console


# Use an exception as info (but don't raise it):
def func_b(i: int) -> Result[int, ZeroDivisionError]:
    if i == 0:
        return Err(ZeroDivisionError(f"func_b({i})"))
    return Ok(i)


def func_c(i: int) -> Result[str, ValueError]:
    if i == -1:
        return Err(ValueError(f"func_c({i})"))
    return Ok(f"func_c({i})")


def composed(
    i: int,
) -> Result[str, str | ZeroDivisionError | ValueError]:
    result_a = func_a(i)
    if isinstance(result_a, Err):
        return result_a

    result_b = func_b(
        result_a.unwrap()  # unwrap gets the value from Ok
    )
    if isinstance(result_b, Err):
        return result_b

    result_c = func_c(result_b.unwrap())
    return result_c


if __name__ == "__main__":
    display(
        inputs := range(-1, 3),
        outputs := [composed(i) for i in inputs],
    )
    console == """
-1: Err(error=ValueError('func_c(-1)'))
0: Err(error=ZeroDivisionError('func_b(0)'))
1: Err(error='func_a(1)')
2: Ok(value='func_c(2)')
"""
