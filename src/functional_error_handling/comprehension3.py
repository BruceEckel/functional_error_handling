#: Comprehension3.py
# Explicit result type
from result import Result, Err, Ok


def f2(i: int) -> Result[int, str]:
    if i == 1:
        return Err("i cannot be 1")
    else:
        return Ok(i * 2)


results = [f2(i) for i in range(3)]
print(results)
"""
[Ok(value=0), Err(error='i cannot be 1'), Ok(value=4)]
"""

for result in results:
    match result:
        case Ok(value):
            print(value)
        case Err(error):
            print(f"Error: {error}")
"""
0
Error: i cannot be 1
4
"""


# Composition: return type enforced
def g(i: int) -> Result[int, str]:
    return f2(i)


print(g(1))
print(g(5))
"""
Err(error='i cannot be 1')
Ok(value=10)
"""
