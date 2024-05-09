#: comprehension6.py
# Using https://github.com/dry-python/returns
from returns.pipeline import is_successful, pipe
from returns.pointfree import bind
from returns.result import Failure, Result, Success, safe
from util import display
from validate_output import console


def reject_1(i: int) -> Result[int, str]:
    if i == 1:
        return Failure(f"reject_1({i = })")
    return Success(i)


# Convert existing function.
# Return type becomes Result[int, ZeroDivisionError]
@safe
def reject_0(i: int) -> int:
    print(f"reject_0({i}) succeeded: {1 / i}")
    return i


def reject_minus_1(i: int) -> Result[str, ValueError]:
    if i == -1:
        return Failure(ValueError(f"c({i =})"))
    return Success(f"reject_minus_1({i})")


composed = pipe(  # type: ignore
    reject_1,
    bind(reject_0),
    bind(reject_minus_1),
)

inputs = range(-1, 3)  # [-1, 0, 1, 2]
outputs = [composed(i) for i in inputs]
console == """
reject_0(-1) succeeded: -1.0
reject_0(2) succeeded: 0.5
"""

display(inputs, outputs)
console == """
-1: <Failure: c(i =-1)>
0: <Failure: division by zero>
1: <Failure: reject_1(i = 1)>
2: <Success: reject_minus_1(2)>
"""

# Extract results, converting failure to None:
with_nones = [r.value_or(None) for r in outputs]
print(str(with_nones))
print(str(list(filter(None, with_nones))))
console == """
[None, None, None, 'reject_minus_1(2)']
['reject_minus_1(2)']
"""

# Another way to extract results:
for r in outputs:
    if is_successful(r):
        print(f"{r.unwrap() = }")
    else:
        print(f"{r.failure() = }")
console == """
r.failure() = ValueError('c(i =-1)')
r.failure() = ZeroDivisionError('division by zero')
r.failure() = 'reject_1(i = 1)'
r.unwrap() = 'reject_minus_1(2)'
"""
