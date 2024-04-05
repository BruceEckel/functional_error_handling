#: composed.py
from returns.result import Result, Success, Failure, attempt
from returns.pipeline import pipe, is_successful
from returns.pointfree import bind
from typing import Callable

# Is there a way to catch an exception and convert it to a typed Failure?


def a(arg: int) -> Result[int, str]:
    if arg == 1:
        return Failure(f"a({arg = })")
    return Success(arg)


# Convert existing function:
@attempt
def b(arg: int) -> int:  # becomes Result[int, int]
    print(f"b({arg}): {1 / arg}")
    return arg


# Use an exception (but don't raise it):
def c(arg: int) -> Result[str, ValueError]:
    if arg == -1:
        return Failure(ValueError(f"c({arg = })"))
    return Success(f"{arg}!")


composed: Callable[[int], Result[str, ValueError | str | int]] = pipe(
    a,
    bind(b),
    bind(c),
)

inputs = range(-1, 3)
print(f"inputs = {list(inputs)}")
outputs = [composed(i) for i in inputs]

for e in zip(inputs, outputs):
    print(f"{e[0]:>2}: {e[1]}")

# Extract results, converting failure to None:
outputs2 = [r.value_or(None) for r in outputs]
print(outputs2)
print(list(filter(None, outputs2)))

# Another way to extract results:
for r in outputs:
    if is_successful(r):
        print(f"{r.unwrap() = }")
    else:
        print(f"{r.failure() = }")

# fmt: off
def do_notation(i: int):
    return Result.do(
        cr
        for ar in a(i)
        for br in b(ar)
        for cr in c(br)
    )


print([do_notation(i) for i in inputs])
