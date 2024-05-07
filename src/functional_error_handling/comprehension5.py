#: comprehension5.py
# Using https://github.com/dry-python/returns
from returns.pipeline import is_successful, pipe
from returns.pointfree import bind
from returns.result import Failure, Result, Success, safe
from validate_output import console


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


def c(i: int) -> Result[str, ValueError]:
    if i == -1:
        return Failure(ValueError(f"c({i =})"))
    return Success(f"c({i})")


composed = pipe(  # type: ignore
    a,
    bind(b),
    bind(c),
)

inputs = range(-1, 3)  # [-1, 0, 1, 2]
outputs = [composed(i) for i in inputs]
console == """
b(-1): -1.0
b(2): 0.5
"""

for inp, outp in zip(inputs, outputs):
    print(f"{inp:>2}: {outp}")
console == """
-1: <Failure: c(i =-1)>
 0: <Failure: division by zero>
 1: <Failure: a(i = 1)>
 2: <Success: c(2)>
"""

# Extract results, converting failure to None:
with_nones = [r.value_or(None) for r in outputs]
print(str(with_nones))
print(str(list(filter(None, with_nones))))
console == """
[None, None, None, 'c(2)']
['c(2)']
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
r.failure() = 'a(i = 1)'
r.unwrap() = 'c(2)'
"""
