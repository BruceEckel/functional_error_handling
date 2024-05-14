# Functional Error Handling
<!-- #[code_location] ./src/functional_error_handling -->
Bruce Eckel
Github: BruceEckel/functional_error_handling

---

- Github: BruceEckel/functional_error_handling
    - These slides (Slides.md for Obsidian)
    - Paper: depth in things I can only touch on
    - Code examples + tools

- Requires Python type annotations + checker

---
#### Acknowledgements

- Helping Bill Frasure & James Ward on
> Effect-Oriented Programming
- Interviews that James and I have done for the [Happy Path Programming podcast](https://happypathprogramming.com/).
- ChatGPT: Unreliable but still very useful

---

- Most of what we've been working towards in programming—whether we are aware of it or not—is composability

> Combining smaller pieces into bigger pieces

- Effortlessly assemble components in the same way a child assembles Legos

---
### Steps to Composability
- Gotos -> Functions
- Modules
- Inheritance Breaks Encapsulation

---
### Error Handling

- Different approaches 
- Usually global solutions with race conditions
- Hard to compose
- The domain of the OS or the language?
    - Initial OS experiments, including resumption

---
### Exceptions

- In the language domain: closer to the problem
- Standard way to report errors
- Errors can't be ignored
- Added recovery

---
- In the small, exceptions seem to work well
- Scaling up (composing) reveals problems

---
### 1. Not Part of the Type System

- Don’t know what exceptions will emerge
- The function can start throwing new ones
- C++ and Java tried *exception specifications*—didn't work
 
---
### 2. Conflates Categories

- Recoverable
- Panic: program can't continue
    - Treated the same as recoverable
    - Unecessary overhead

---
### 3. Exceptions Destroy Partial Calculations

1. Computationally wasteful, especially with large calculations
2. Makes debugging harder

---
```python
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
```

---
### The Functional Approach

- Stop using exceptions
- Functions return a “package” combining the answer + potential error
- We can do this with a *type union*:

---
```python
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
```

---
### Creating a New Return Type

---
```python
#: result.py
# Generic Result with Success & Failure subtypes
from dataclasses import dataclass
from typing import Generic, TypeVar

ANSWER = TypeVar("ANSWER")  # Generic parameters
ERROR = TypeVar("ERROR")


@dataclass(frozen=True)
class Result(Generic[ANSWER, ERROR]):
    pass


@dataclass(frozen=True)
class Success(Result[ANSWER, ERROR]):
    answer: ANSWER  # Usage: return Success(answer)

    def unwrap(self) -> ANSWER:
        return self.answer


@dataclass(frozen=True)
class Failure(Result[ANSWER, ERROR]):
    error: ERROR  # Usage: return Failure(error)
```

### Incorporate `Result`

---
```python
#: example3.py
# Result type returns Success/Failure
from pprint import pprint

from returns.result import Failure, Result, Success
from validate_output import console


def func_a(i: int) -> Result[int, str]:
    if i == 1:
        return Failure(f"func_a({i})")
    return Success(i)


if __name__ == "__main__":
    pprint([(i, func_a(i)) for i in range(5)])
    console == """
[(0, <Success: 0>),
 (1, <Failure: func_a(1)>),
 (2, <Success: 2>),
 (3, <Success: 3>),
 (4, <Success: 4>)]
"""
```

---
### Composing with `Result`

---
```python
#: example4.py
# Composing functions
# Using https://github.com/dry-python/returns
from pprint import pprint

from example3 import func_a
from returns.result import Failure, Result, Success, safe
from validate_output import console


# Use an exception as info (but don't raise it):
def func_b(i: int) -> Result[int, ValueError]:
    if i == 2:
        return Failure(ValueError(f"func_b({i})"))
    return Success(i)


# Convert exception to Failure:
def func_c(i: int) -> Result[int, ZeroDivisionError]:
    try:
        1 / (i - 3)
    except ZeroDivisionError as e:
        return Failure(
            ZeroDivisionError(f"func_c({i}): {e}")
        )
    return Success(i)


@safe  # Convert existing function
def func_d(i: int) -> str:  # Result[str, ZeroDivisionError]
    1 / i
    return f"func_d({i})"


def composed(
    i: int,
) -> Result[str, str | ValueError | ZeroDivisionError]:
    result_a = func_a(i)
    if isinstance(result_a, Failure):
        return result_a

    # unwrap() gets the answer from Success:
    result_b = func_b(result_a.unwrap())
    if isinstance(result_b, Failure):
        return result_b

    result_c = func_c(result_b.unwrap())
    if isinstance(result_c, Failure):
        return result_c

    return func_d(result_c.unwrap())


if __name__ == "__main__":
    pprint([(i, composed(i)) for i in range(5)])
    console == """
[(0, <Failure: division by zero>),
 (1, <Failure: func_a(1)>),
 (2, <Failure: func_b(2)>),
 (3, <Failure: func_c(3): division by zero>),
 (4, <Success: func_d(4)>)]
"""
```

- Failure causes a short-circuit
- Returns an `Failure` that tells you exactly what happened
- Can't ignore it
- Close to the origin where information is highest

---
### Simplifying Composition with `bind`

```python
#: result_with_bind.py
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

ANSWER = TypeVar("ANSWER")
ERROR = TypeVar("ERROR")


@dataclass(frozen=True)
class Result(Generic[ANSWER, ERROR]):
    def bind(
        self, func: Callable[[ANSWER], "Result"]
    ) -> "Result[ANSWER, ERROR]":
        if isinstance(self, Success):
            return func(self.unwrap())
        return self  # Pass the Failure forward


@dataclass(frozen=True)
class Success(Result[ANSWER, ERROR]):
    answer: ANSWER

    def unwrap(self) -> ANSWER:
        return self.answer


@dataclass(frozen=True)
class Failure(Result[ANSWER, ERROR]):
    error: ERROR
```


---

```python
#: example5.py
# Simplifying composition with bind
from pprint import pprint

from example4 import func_a, func_b, func_c, func_d
from returns.result import Result
from validate_output import console


def composed(
    i: int,
) -> Result[str, str | ZeroDivisionError | ValueError]:
    # fmt: off
    return (
        func_a(i)
        .bind(func_b)
        .bind(func_c)
        .bind(func_d)
    )


if __name__ == "__main__":
    pprint([(i, composed(i)) for i in range(5)])
    console == """
[(0, <Failure: division by zero>),
 (1, <Failure: func_a(1)>),
 (2, <Failure: func_b(2)>),
 (3, <Failure: func_c(3): division by zero>),
 (4, <Success: func_d(4)>)]
"""
```

---

### Handling Multiple Arguments

---
```python
#: example6.py
# Multiple arguments in composition
from pprint import pprint

from example4 import func_a, func_b, func_c
from returns.result import Result
from validate_output import console


def add(first: int, second: int, third: int) -> str:
    return (
        f"add({first} + {second} + {third}):"
        f" {first + second + third}"
    )


def composed(
    i: int, j: int
) -> Result[str, str | ZeroDivisionError | ValueError]:
    # fmt: off
    return Result.do(
        add(first, second, third)
        for first in func_a(i)
        for second in func_b(j)
        for third in func_c(i + j)
    )


pprint(
    [
        (args, composed(*args))
        for args in [(1, 5), (7, 2), (2, 1), (7, 5)]
    ]
)
console == """
[((1, 5), <Failure: func_a(1)>),
 ((7, 2), <Failure: func_b(2)>),
 ((2, 1), <Failure: func_c(3): division by zero>),
 ((7, 5), <Success: add(7 + 5 + 12): 24>)]
"""
```

---
### Functional Error Handling is Happening

- Already in Rust, Kotlin, and recent versions of C++
- Errors are part of the type system
- Far more difficult for an error to slip through the cracks
- Benefits make it worth adopting a library like `Results`

---
- Open spaces session if you want to Q&A
