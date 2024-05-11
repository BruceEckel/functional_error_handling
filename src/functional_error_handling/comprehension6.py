#: comprehension6.py
# Using https://github.com/dry-python/returns
from returns.pipeline import is_successful, pipe
from returns.pointfree import bind
from returns.result import Failure, Result, Success, safe
from util import display
from validate_output import console


def func_a(i: int) -> Result[int, str]:
    if i == 1:
        return Failure(f"func_a({i = })")
    return Success(i)


# Convert existing function.
# Return type becomes Result[int, ZeroDivisionError]
@safe
def func_b(i: int) -> int:
    print(f"func_b({i}) succeeded: {1 / i}")
    return i


def func_c(i: int) -> Result[str, ValueError]:
    if i == -1:
        return Failure(ValueError(f"func_c({i =})"))
    return Success(f"func_c({i})")


composed = pipe(  # type: ignore
    func_a,
    bind(func_b),
    bind(func_c),
)

inputs = range(-1, 3)  # [-1, 0, 1, 2]
outputs = [composed(i) for i in inputs]
console == """
func_b(-1) succeeded: -1.0
func_b(2) succeeded: 0.5
"""

display(inputs, outputs)
console == """
-1: <Failure: func_c(i =-1)>
0: <Failure: division by zero>
1: <Failure: func_a(i = 1)>
2: <Success: func_c(2)>
"""

# Extract results, converting failure to None:
with_nones = [r.value_or(None) for r in outputs]
print(str(with_nones))
print(str(list(filter(None, with_nones))))
console == """
[None, None, None, 'func_c(2)']
['func_c(2)']
"""

# Another way to extract results:
for r in outputs:
    if is_successful(r):
        print(f"{r.unwrap() = }")
    else:
        print(f"{r.failure() = }")
console == """
r.failure() = ValueError('func_c(i =-1)')
r.failure() = ZeroDivisionError('division by zero')
r.failure() = 'func_a(i = 1)'
r.unwrap() = 'func_c(2)'
"""
