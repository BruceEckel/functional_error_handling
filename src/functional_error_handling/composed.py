#: composed.py
# Is there a way to have multiple arguments to composed()?
from returns.result import Result, Success, Failure, safe
from returns.pipeline import flow
from returns.pointfree import bind
from test import test


def a(i: int) -> Result[int, str]:
    if i == 1:
        return Failure(f"a({i = })")
    return Success(i)


# Convert existing function.
# Return type becomes Result[int, ZeroDivisionError]
@safe
def b(i: int) -> int:
    print(f"b({i}): {1 / i}")
    return i


# Use an exception for extra info (but don't raise it):
def c(i: int) -> Result[str, ValueError]:
    if i == -1:
        return Failure(ValueError(f"c({i = })"))
    return Success(f"{i}!")


def composed(i: int) -> Result[str, str | ZeroDivisionError | ValueError]:
    return flow(
        i,
        a,
        bind(b),
        bind(c),
    )


print(test(composed))
