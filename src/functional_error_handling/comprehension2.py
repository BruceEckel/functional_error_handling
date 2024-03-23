#: Comprehension2.py
# Type union aka Sum Type
# Not terrible, but explicit type seems better...


def f3(i: int) -> int | str:  # Sum type
    if i == 3:
        return "i cannot be 3"
    else:
        return i * 2


results = [f3(i) for i in range(5)]
print(results)
"""
[0, 2, 4, 'i cannot be 3', 8]
"""

for result in results:
    match result:
        case int(value):
            print(value)
        case str(error):
            print(f"Error: {error}")
"""
0
2
4
Error: i cannot be 3
8
"""


# Composition: return type enforced
def g(i: int) -> int | str:
    return f3(i)


print(g(1))
print(g(5))
"""
2
10
"""
