#: Comprehension2.py
# Type union aka Sum Type
# Success vs error is not clear


def f3(i: int) -> int | str:  # Sum type
    if i == 1:
        return "i cannot be 1"
    else:
        return i * 2


results = [f3(i) for i in range(3)]
print(results)
"""
[0, 'i cannot be 1', 4]
"""

for result in results:
    match result:
        case int(value):
            print(value)
        case str(error):
            print(f"Error: {error}")
"""
0
Error: i cannot be 1
4
"""


# Composition: return type enforced
def g(i: int) -> int | str:
    return f3(i)


print(g(1))
print(g(5))
"""
i cannot be 1
10
"""
