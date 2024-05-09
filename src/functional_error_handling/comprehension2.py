#: comprehension2.py
# Type union aka Sum Type
# Success vs error is not clear
from validate_output import console


def reject_1(i: int) -> int | str:  # Sum type
    if i == 1:
        return "i is 1"
    return i * 2


print(outputs := [reject_1(i) for i in range(3)])
console == """
[0, 'i is 1', 4]
"""

for r in outputs:
    match r:
        case int(value):
            print(f"{value = }")
        case str(error):
            print(f"{error = }")
console == """
value = 0
error = 'i is 1'
value = 4
"""


# Composition: return type enforced
def g(i: int) -> int | str:
    return reject_1(i)


print(g(1))
print(g(5))
console == """
i is 1
10
"""
