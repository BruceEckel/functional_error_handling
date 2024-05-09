#: comprehension5.py
# Simplifying composition with and_then
from comprehension4 import reject_0, reject_1, reject_minus_1
from result import Result
from validate_output import console


def composed(i: int) -> Result[str, str | ZeroDivisionError | ValueError]:
    return reject_1(i).and_then(reject_0).and_then(reject_minus_1)


inputs = range(-1, 3)
print(outputs := [composed(i) for i in inputs])
console == """
[Err(error=ValueError(-1)), Err(error=ZeroDivisionError()), Err(error='i is 1'), Ok(value='2#')]
"""

for inp, outp in zip(inputs, outputs):
    print(f"{inp:>2}: {outp}")
console == """
-1: Err(error=ValueError(-1))
 0: Err(error=ZeroDivisionError())
 1: Err(error='i is 1')
 2: Ok(value='2#')
"""
