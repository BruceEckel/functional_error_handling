#: example2.py
# Type union aka Sum Type
# Success vs error is not clear
from util import display
from validate_output import console


def func_a(i: int) -> int | str:  # Sum type
    if i == 1:
        return f"func_a({i})"
    return i


display(
    inputs := range(3),
    outputs := [func_a(i) for i in inputs],
)
console == """
0: 0
1: func_a(1)
2: 2
"""

for r in outputs:
    match r:
        case int(answer):
            print(f"{answer = }")
        case str(error):
            print(f"{error = }")
console == """
answer = 0
error = 'func_a(1)'
answer = 2
"""
