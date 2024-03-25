#: Comprehension1.py
# Exception produces no results, stops everything


def f1(i: int) -> int:
    if i == 1:
        raise ValueError("i cannot be 1")
    else:
        return i * 2


print([f1(i) for i in range(3)])
"""
Traceback (most recent call last):
  File "C:\git\functional_error_handling\src\functional_error_handling\comprehension1.py", line 12, in <module>
    print([f1(i) for i in range(3)])
           ^^^^^
  File "C:\git\functional_error_handling\src\functional_error_handling\comprehension1.py", line 7, in f1
    raise ValueError("i cannot be 1")
ValueError: i cannot be 1
"""
