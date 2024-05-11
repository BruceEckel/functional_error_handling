#: comprehension1.py
# Exception produces no results, stops everything


def func_a(i: int) -> int:
    if i == 1:
        raise ValueError(f"func_a({i})")
    return i


result = [func_a(i) for i in range(3)]
print(result)
"""
Traceback (most recent call last):
  ...
ValueError: i is 1
"""
