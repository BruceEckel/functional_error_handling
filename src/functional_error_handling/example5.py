#: example5.py
# Simplifying composition with bind
from pprint import pprint

from example4 import func_a, func_b, func_c, func_d
from returns.result import Result
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
    pprint([(i, composed(i)) for i in range(5)])
    console == """
[(0, <Failure: division by zero>),
 (1, <Failure: func_a(1)>),
 (2, <Failure: func_b(2)>),
 (3, <Failure: func_c(3): division by zero>),
 (4, <Success: func_d(4)>)]
"""
