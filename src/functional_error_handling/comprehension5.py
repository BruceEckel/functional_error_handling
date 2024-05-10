#: comprehension5.py
# Simplifying composition with and_then
from comprehension4 import reject_0, reject_1, reject_minus_1
from result import Result
from util import display
from validate_output import console


def composed(
    i: int,
) -> Result[str, str | ZeroDivisionError | ValueError]:
    # fmt: off
    return (
        reject_1(i)
        .and_then(reject_0)
        .and_then(reject_minus_1)
    )


# fmt: off
display(inputs := range(-1, 3),
    [composed(i) for i in inputs])
console == """
-1: Err(error=ValueError(-1))
0: Err(error=ZeroDivisionError())
1: Err(error='i is 1')
2: Ok(value='2#')
"""
