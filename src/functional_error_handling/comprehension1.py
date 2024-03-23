#: Comprehension1.py
# Exception produces no results, stops everything


def f1(i: int) -> int:
    if i == 3:
        raise ValueError("i cannot be 3")
    else:
        return i * 2


print([f1(i) for i in range(5)])
"""
Traceback (most recent call last):
  File "C:\git\functional_error_handling\src\functional_error_handling\comprehension1.py", line 8, in <module>
    print([f1(i) for i in range(5)])
           ^^^^^
  File "C:\git\functional_error_handling\src\functional_error_handling\comprehension1.py", line 3, in f1
    raise ValueError("i cannot be 3")
ValueError: i cannot be 3
"""
