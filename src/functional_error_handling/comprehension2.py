#: comprehension2.py
# Type union aka Sum Type
# Success vs error is not clear
from util import display
from validate_output import console


def reject_1(i: int) -> int | str:  # Sum type
    if i == 1:
        return "i is 1"
    return i * 2


inputs = range(3)  # [0, 1, 2]
outputs = [reject_1(i) for i in inputs]
display(inputs, outputs)
console == """
0: 0
1: i is 1
2: 4
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


# Return type enforced
def composed(i: int) -> int | str:
    return reject_1(i)


print(composed(1))
print(composed(5))
console == """
i is 1
10
"""
