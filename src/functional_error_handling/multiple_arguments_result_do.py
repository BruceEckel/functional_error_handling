#: multiple_arguments_result_do.py
from returns.result import Result, Success, Failure


def add(first: int, second: int) -> int:
    return first + second


def not_one(i: int) -> Result[int, ValueError]:
    if i == 1:
        return Failure(ValueError(f"not_one: {i} is 1"))
    return Success(i * 10)


def not_two(i: int) -> Result[int, ValueError]:
    if i == 2:
        return Failure(ValueError(f"not_two: {i} is 2"))
    return Success(i * 100)


def do_add(i: int, j: int) -> int:
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
