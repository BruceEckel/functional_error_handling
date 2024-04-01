# composed.py
from returns.result import Result, Success, Failure
from returns.pipeline import pipe
from returns.pointfree import bind
from typing import Callable


def f4(arg: int) -> Result[int, str]:
    if arg == 1:
        return Failure(f"f4({arg = })")
    else:
        return Success(arg * 2)


def f5(arg: int) -> Result[str, str]:
    if arg == 0:
        return Failure(f"f5({arg = })")
    return Success(str(arg))


def f6(arg: str) -> Result[str, ValueError]:
    if arg == "-2":
        return Failure(ValueError(f"f6({arg = })"))
    return Success(arg + "!")


composed: Callable[[int], Result[str, ValueError | str]] = pipe(
    f4,
    bind(f5),
    bind(f6),
)


print([composed(i) for i in range(-1, 3)])
