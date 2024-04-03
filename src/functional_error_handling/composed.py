#: composed.py
from returns.result import Result, Success, Failure, attempt
from returns.pipeline import pipe, is_successful
from returns.pointfree import bind
from typing import Callable

# Is there a way to catch an exception and convert it to a typed Failure?


def f4(arg: int) -> Result[int, str]:
    if arg == 1:
        return Failure(f"f4({arg = })")
    return Success(arg)


# Convert an existing function:
@attempt
def f5(arg: int) -> int:  # becomes: Result[int, int]
    print(f"f5: {arg = }, {1 / arg = }")
    return arg


# This might be redundant
def f6(arg: int) -> Result[str, str]:
    if arg == 2:
        return Failure(f"f6({arg = })")
    return Success(str(arg))


# Use an exception (but don't raise it):
def f7(arg: str) -> Result[str, ValueError]:
    if arg == "-1":
        return Failure(ValueError(f"f7({arg = })"))
    return Success(arg + "!")


# Is Result type correct here?
composed: Callable[[int], Result[str, ValueError | str]] = pipe(
    f4,
    bind(f5),
    bind(f6),
    bind(f7),
)

inputs = range(-1, 4)
print(f"inputs = {list(inputs)}")
outputs = [composed(i) for i in inputs]

for e in zip(inputs, outputs):
    print(f"{e[0]:>2}: {e[1]}")

# Extract results, converting failure to None:
print([r.value_or(None) for r in outputs])

# Another way to extract results:
for r in outputs:
    if is_successful(r):
        print(f"{r.unwrap() = }")
    else:
        print(f"{r.failure() = }")
