#: comprehension4.py
# Composing functions
from result import Err, Ok, Result
from validate_output import console


def reject_1(i: int) -> Result[int, str]:
    if i == 1:
        return Err("i is 1")
    return Ok(i)


# Use an exception as info (but don't raise it):
def reject_0(i: int) -> Result[int, ZeroDivisionError]:
    if i == 0:
        return Err(ZeroDivisionError())
    return Ok(i)


def reject_minus_1(i: int) -> Result[str, ValueError]:
    if i == -1:
        return Err(ValueError(i))
    return Ok(f"{i}#")


def composed(i: int) -> Result[str, str | ZeroDivisionError | ValueError]:
    result_a = reject_1(i)
    if isinstance(result_a, Err):
        return result_a

    result_b = reject_0(result_a.unwrap())  # unwrap gets the value from Ok
    if isinstance(result_b, Err):
        return result_b

    result_c = reject_minus_1(result_b.unwrap())
    return result_c


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
