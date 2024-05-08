#: comprehension5.py
# Simplifying composition with and_then
from result import Result
from validate_output import console
from comprehension4 import a, b, c


def composed(i: int) -> Result[str, str | ZeroDivisionError | ValueError]:
    return a(i).and_then(b).and_then(c)


inputs = range(-1, 3)
print(outputs := [composed(i) for i in inputs])
console == """
[Err(error=ValueError(-1)), Err(error=ZeroDivisionError()), Err(error='i cannot be 1'), Ok(value='2#')]
"""

for inp, outp in zip(inputs, outputs):
    print(f"{inp:>2}: {outp}")
console == """
-1: Err(error=ValueError(-1))
 0: Err(error=ZeroDivisionError())
 1: Err(error='i cannot be 1')
 2: Ok(value='2#')
"""
