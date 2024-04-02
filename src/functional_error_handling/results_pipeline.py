#: results_pipeline.py
# Adapted from https://returns.readthedocs.io/en/latest/pages/pipeline.html
from returns.pipeline import pipe
from returns.result import Result, Success, Failure
from returns.pointfree import bind
from typing import Callable


def regular_function(arg: int) -> float:
    return float(arg)


def returns_container(arg: float) -> Result[str, ValueError]:
    if arg != 0:
        return Success(str(arg))
    return Failure(ValueError("Wrong arg"))


def also_returns_container(arg: str) -> Result[str, ValueError]:
    return Success(arg + "!")


transaction: Callable[[int], Result[str, ValueError]] = pipe(
    regular_function,
    returns_container,
    bind(also_returns_container),
)

print(transaction(1))  # run the composed function pipeline
