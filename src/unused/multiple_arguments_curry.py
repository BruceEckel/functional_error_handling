#: multiple_arguments_curry.py
from returns.curry import curry
from returns.maybe import Some
from returns.pipeline import flow


@curry
def add_curried(first: int, second: int) -> int:
    return first + second


def add(i: int, j: int) -> int:
    return flow(
        Some(add_curried),
        Some(i).apply,
        Some(j).apply,
    )


print(add(1, 2))  # Some(3)
