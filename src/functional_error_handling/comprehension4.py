#: comprehension4.py
# Composing functions
from result import Result, Err, Ok
from validate_output import console


def a(i: int) -> Result[int, str]:
    if i == 1:
        return Err("i cannot be 1")
    else:
        return Ok(i)


# Use an exception as info (but don't raise it):
def b(i: int) -> Result[int, ZeroDivisionError]:
    if i == 0:
        return Err(ZeroDivisionError())
    return Ok(i)


def c(i: int) -> Result[str, ValueError]:
    if i == -1:
        return Err(ValueError(i))
    return Ok(f"{i}#")


def composed(i: int) -> Result[str, str | ZeroDivisionError | ValueError]:
    result_a = a(i)
    if isinstance(result_a, Err):
        return result_a

    result_b = b(result_a.unwrap())  # unwrap gets the value from Ok
    if isinstance(result_b, Err):
        return result_b

    result_c = c(result_b.unwrap())
    return result_c


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
