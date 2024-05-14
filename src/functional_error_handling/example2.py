#: example2.py
# Type union aka Sum Type
# Success vs error is not clear
from validate_output import console


def func_a(i: int) -> int | str:  # Sum type
    if i == 1:
        return f"func_a({i})"
    return i


print(outputs := [(i, func_a(i)) for i in range(5)])
console == """
[(0, 0), (1, 'func_a(1)'), (2, 2), (3, 3), (4, 4)]
"""

for _, r in outputs:
    match r:
        case int(answer):
            print(f"{answer = }")
        case str(error):
            print(f"{error = }")
console == """
answer = 0
error = 'func_a(1)'
answer = 2
answer = 3
answer = 4
"""
