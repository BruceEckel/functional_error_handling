#: Comprehension2_validate.py
# Type union aka Sum Type
# Success vs error is not clear
from validate_output import validate


def f2(i: int) -> int | str:  # Sum type
    if i == 1:
        return "i cannot be 1"
    else:
        return i * 2


print(outputs := [f2(i) for i in range(3)])
"""=
[0, 'i cannot be 1', 4]
"""

for r in outputs:
    match r:
        case int(value):
            print(value)
        case str(error):
            print(f"Error: {error}")
"""=
0
Error: i cannot be 1
4
"""


# Composition: return type enforced
def g(i: int) -> int | str:
    return f2(i)


print(g(1))
print(g(5))
"""=
i cannot be 1
10
"""

# validate()
