from result import Result, Err, Ok


def f2(i: int) -> Result[int, str]:
    if i == 3:
        return Err("i cannot be 3")
    else:
        return Ok(i * 2)


results = [f2(i) for i in range(5)]
print(results)
"""
[Ok(value=0), Ok(value=2), Ok(value=4), Err(error='i cannot be 3'), Ok(value=8)]
"""

for result in results:
    match result:
        case Ok(value):
            print(value)
        case Err(error):
            print(f"Error: {error}")
"""
0
2
4
Error: i cannot be 3
8
"""


# Composition: return type enforced
def g(i: int) -> Result[int, str]:
    return f2(i)


print(g(1))
print(g(5))
"""
Ok(value=2)
Ok(value=10)
"""
