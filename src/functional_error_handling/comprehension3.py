#: comprehension3.py
# Explicit result type
from result import Failure, Success, Result
from util import display
from validate_output import console


def func_a(i: int) -> Result[int, str]:
    if i == 1:
        return Failure(f"func_a({i})")
    return Success(i)


if __name__ == "__main__":
    display(
        inputs := range(3),
        outputs := [func_a(i) for i in inputs],
    )
    console == """
0: Success(answer=0)
1: Failure(error='func_a(1)')
2: Success(answer=2)
"""
