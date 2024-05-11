#: comprehension6.py
# Using https://github.com/dry-python/returns
from returns.pipeline import is_successful, pipe
from returns.pointfree import bind
from returns.result import Failure, Result, Success, safe
from util import display
from validate_output import console


def func_a(i: int) -> Result[int, str]:
    if i == 1:
        return Failure(f"func_a({i})")
    return Success(i)


def func_b(i: int) -> Result[int, ZeroDivisionError]:
    if i == 0:
        return Failure(ZeroDivisionError(f"func_b({i})"))
    return Success(i)


# Convert existing function.
# Return type becomes Result[str, ValueError]
@safe
def func_c(i: int) -> str:
    if i == -1:
        return ValueError(f"func_c({i})")
    return f"func_c({i})"


composed = pipe(  # type: ignore
    func_a,
    bind(func_b),
    bind(func_c),
)

if __name__ == "__main__":
    display(
        inputs := range(-1, 3),
        outputs := [composed(i) for i in inputs],
    )
    console == """
-1: <Success: func_c(-1)>
0: <Failure: func_b(0)>
1: <Failure: func_a(1)>
2: <Success: func_c(2)>
"""

    # Extract results, converting failure to None:
    with_nones = [r.value_or(None) for r in outputs]
    print(str(with_nones))
    print(str(list(filter(None, with_nones))))
    console == """
[ValueError('func_c(-1)'), None, None, 'func_c(2)']
[ValueError('func_c(-1)'), 'func_c(2)']
"""

    # Another way to extract results:
    for r in outputs:
        if is_successful(r):
            print(f"{r.unwrap() = }")
        else:
            print(f"{r.failure() = }")
    console == """
r.unwrap() = ValueError('func_c(-1)')
r.failure() = ZeroDivisionError('func_b(0)')
r.failure() = 'func_a(1)'
r.unwrap() = 'func_c(2)'
"""
