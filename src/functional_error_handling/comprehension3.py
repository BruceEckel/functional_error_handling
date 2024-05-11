#: comprehension3.py
# Explicit result type
from result import Err, Ok, Result
from validate_output import console


def func_a(i: int) -> Result[int, str]:
    if i == 1:
        return Err("i is 1")
    return Ok(i)


print(outputs := [func_a(i) for i in range(3)])
console == """
[Ok(value=0), Err(error='i is 1'), Ok(value=2)]
"""

for r in outputs:
    match r:
        case Ok(value):
            print(f"{value = }")
        case Err(error):
            print(f"{error = }")
console == """
value = 0
error = 'i is 1'
value = 2
"""
