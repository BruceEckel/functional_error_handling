#: comprehension3.py
# Explicit result type
from result import Err, Ok, Result
from util import display
from validate_output import console


def func_a(i: int) -> Result[int, str]:
    if i == 1:
        return Err(f"func_a({i})")
    return Ok(i)


if __name__ == "__main__":
    display(
        inputs := range(3),
        outputs := [func_a(i) for i in inputs],
    )
    console == """
0: Ok(value=0)
1: Err(error='func_a(1)')
2: Ok(value=2)
"""
