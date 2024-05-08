#: comprehension1.py
# Exception produces no results, stops everything


def f1(i: int) -> int:
    if i == 1:
        raise ValueError("i is 1")
    else:
        return i * 2


result = [f1(i) for i in range(3)]
print(result)
"""
Traceback (most recent call last):
  ...
ValueError: i is 1
"""
