#: composed.py
from returns.result import Result, Success, Failure, attempt
from returns.pipeline import pipe, is_successful
from returns.pointfree import bind
from typing import Callable


def f4(arg: int) -> Result[int, str]:
    if arg == 1:
        return Failure(f"f4({arg = })")
    else:
        return Success(arg * 2)


@attempt
def divzero(arg: int) -> float:  # becomes: Result[float, int]
    # return Success(10 / arg)
    return 10 / arg


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
    # bind(divzero),
    bind(f5),
    bind(f6),
)

results = [composed(i) for i in range(-1, 3)]

print(results)
print([r.value_or(None) for r in results])

for r in results:
    if is_successful(r):
        print(f"{r.unwrap() = }")
    else:
        print(f"{r.failure() = }")
