#: comprehension5.py
# Simplifying composition with bind
from comprehension4 import func_a, func_b, func_c
from returns.result import Result
from util import display
from validate_output import console


def composed(
    i: int,
) -> Result[str, str | ZeroDivisionError | ValueError]:
    # fmt: off
    return (
        func_a(i)
        .bind(func_b)
        .bind(func_c)
    )


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
