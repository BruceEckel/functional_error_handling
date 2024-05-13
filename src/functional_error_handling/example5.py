#: example5.py
# Simplifying composition with bind
from example4 import func_a, func_b, func_c, func_d
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
        .bind(func_d)
    )


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
