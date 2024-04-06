#: composed.py
# Is there a way to have multiple arguments to compose()?
from returns.result import Result, Success, Failure, safe
from returns.pipeline import flow, is_successful
from returns.pointfree import bind


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


def test(fn, inputs=range(-1, 3)) -> str:
    results = [f"inputs = {list(inputs)}"]
    outputs = [fn(i) for i in inputs]

    for e in zip(inputs, outputs):
        results.append(f"{e[0]:>2}: {e[1]}")

    # Extract results, converting failure to None:
    outputs2 = [r.value_or(None) for r in outputs]

    results.append(str(outputs2))
    results.append(str(list(filter(None, outputs2))))

    # Another way to extract results:
    for r in outputs:
        if is_successful(r):
            results.append(f"{r.unwrap() = }")
        else:
            results.append(f"{r.failure() = }")

    return "\n".join(results)


print(test(composed))

# fmt: off
def do_notation(i: int):
    return Result.do(
        cr
        for ar in a(i)
        for br in b(ar)
        for cr in c(br)
    )

assert test(do_notation) == test(composed)
