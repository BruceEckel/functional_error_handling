#: comprehension3.py
# Explicit result type
from result import Result, Err, Ok
from validate_output import console


def f3(i: int) -> Result[int, str]:
    if i == 1:
        return Err("i cannot be 1")
    else:
        return Ok(i * 2)


print(outputs := [f3(i) for i in range(3)])
console == """
[Ok(value=0), Err(error='i cannot be 1'), Ok(value=4)]
"""

for r in outputs:
    match r:
        case Ok(value):
            print(f"{value = }")
        case Err(error):
            print(f"{error = }")
console == """
value = 0
error = 'i cannot be 1'
value = 4
"""


# Composition: return type enforced
def g(i: int) -> Result[int, str]:
    return f3(i)


print(g(1))
print(g(5))
console == """
Err(error='i cannot be 1')
Ok(value=10)
"""
