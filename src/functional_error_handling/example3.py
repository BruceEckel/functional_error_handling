#: example3.py
# Result type returns Success/Failure
from returns.result import Failure, Result, Success
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
0: <Success: 0>
1: <Failure: func_a(1)>
2: <Success: 2>
"""
