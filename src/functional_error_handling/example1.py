#: example1.py
# Exception throws everything away


def func_a(i: int) -> int:
    if i == 1:
        raise ValueError(f"func_a({i})")
    return i


result = [func_a(i) for i in range(3)]
print(result)
"""
Traceback (most recent call last):
  ...
ValueError: func_a(1)
"""
