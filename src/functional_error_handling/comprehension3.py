#: Comprehension3.py
# Explicit result type
from result import Result, Err, Ok
from typing import reveal_type


def f3(i: int) -> Result[int, str]:
    if i == 1:
        return Err("i cannot be 1")
    else:
        return Ok(i * 2)


results = [f3(i) for i in range(3)]
print(results)
"""
[Ok(value=0), Err(error='i cannot be 1'), Ok(value=4)]
"""

for result in results:
    reveal_type(result)
    match result:
        case Ok(value):
            print(f"{value = }")
        case Err(error):
            print(f"{error = }")
"""
Runtime type is 'Ok'
value = 0
Runtime type is 'Err'
error = 'i cannot be 1'
Runtime type is 'Ok'
value = 4
"""


# Composition: return type enforced
def g(i: int) -> Result[int, str]:
    return f3(i)


print(g(1))
print(g(5))
"""
Err(error='i cannot be 1')
Ok(value=10)
"""
