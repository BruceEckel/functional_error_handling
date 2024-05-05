#: multiple_arguments.py
from returns.result import Result, Success, Failure
from validate_output import console


def not_one(i: int) -> Result[int, ValueError]:
    if i == 1:
        return Failure(ValueError(f"not_one: {i = }"))
    return Success(i * 10)


def not_two(j: int) -> Result[int, ValueError]:
    if j == 2:
        return Failure(ValueError(f"not_two: {j = }"))
    return Success(j * 100)


def add(first: int, second: int) -> int:
    return first + second


def do_add(i: int, j: int) -> Result[int, ValueError]:
    # fmt: off
    return Result.do(
        add(first, second) 
        for first in not_one(i) 
        for second in not_two(j)
    )


inputs = [(1, 5), (7, 2), (3, 4)]
outputs = [do_add(*inp) for inp in inputs]
for inp, outp in zip(inputs, outputs):
    print(f"{inp}: {outp}")
console == """
(1, 5): <Failure: not_one: i = 1>
(7, 2): <Failure: not_two: j = 2>
(3, 4): <Success: 430>
"""
