#: comprehension5.py
# Simplifying composition with and_then
from comprehension4 import func_a, func_b, func_c
from result import Result
from util import display
from validate_output import console


def composed(
    i: int,
) -> Result[str, str | ZeroDivisionError | ValueError]:
    # fmt: off
    return (
        func_a(i)
        .and_then(func_b)
        .and_then(func_c)
    )


# fmt: off
display(inputs := range(-1, 3),
    [composed(i) for i in inputs])
console == """
-1: Err(error=ValueError('func_c(-1)'))
0: Err(error=ZeroDivisionError('func_b(0)'))
1: Err(error='func_a(1)')
2: Ok(value='2#')
"""
