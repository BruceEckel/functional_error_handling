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
#: comprehension1.py
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
ValueError: i is 1
"""
```

---
### The Functional Approach

- Stop using exceptions
- Functions return a “package” combining the answer + potential error
- We can do this with a *type union*:

---
```python
#: comprehension2.py
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
        case int(value):
            print(f"{value = }")
        case str(error):
            print(f"{error = }")
console == """
value = 0
error = 'func_a(1)'
value = 2
"""
```

---
### Creating a New Return Type

---
```python
#: result_basic.py
# Result with OK & Err subtypes
from dataclasses import dataclass
from typing import Generic, TypeVar

ANSWER = TypeVar("ANSWER")  # Generic parameters
ERROR = TypeVar("ERROR")


@dataclass(frozen=True)
class Result(Generic[ANSWER, ERROR]):
    pass


@dataclass(frozen=True)
class Ok(Result[ANSWER, ERROR]):
    value: ANSWER  # Usage: return Ok(answer)

    def unwrap(self) -> ANSWER:
        return self.value


@dataclass(frozen=True)
class Err(Result[ANSWER, ERROR]):
    error: ERROR  # Usage: return Err(error)
```

### Incorporate `Result`

---
```python
#: comprehension3.py
# Explicit result type
from result import Err, Ok, Result
from util import display
from validate_output import console


def func_a(i: int) -> Result[int, str]:
    if i == 1:
        return Err(f"func_a({i})")
    return Ok(i)


if __name__ == "__main__":
    display(
        inputs := range(3),
        outputs := [func_a(i) for i in inputs],
    )
    console == """
0: Ok(value=0)
1: Err(error='func_a(1)')
2: Ok(value=2)
"""
```

---
### Composing with `Result`

---
```python
#: comprehension4.py
# Composing functions
from comprehension3 import func_a
from result import Err, Ok, Result
from util import display
from validate_output import console


# Use an exception as info (but don't raise it):
def func_b(i: int) -> Result[int, ZeroDivisionError]:
    if i == 0:
        return Err(ZeroDivisionError(f"func_b({i})"))
    return Ok(i)


def func_c(i: int) -> Result[str, ValueError]:
    if i == -1:
        return Err(ValueError(f"func_c({i})"))
    return Ok(f"func_c({i})")


def composed(
    i: int,
) -> Result[str, str | ZeroDivisionError | ValueError]:
    result_a = func_a(i)
    if isinstance(result_a, Err):
        return result_a

    result_b = func_b(
        result_a.unwrap()  # unwrap gets the value from Ok
    )
    if isinstance(result_b, Err):
        return result_b

    result_c = func_c(result_b.unwrap())
    return result_c


if __name__ == "__main__":
    display(
        inputs := range(-1, 3),
        outputs := [composed(i) for i in inputs],
    )
    console == """
-1: Err(error=ValueError('func_c(-1)'))
0: Err(error=ZeroDivisionError('func_b(0)'))
1: Err(error='func_a(1)')
2: Ok(value='func_c(2)')
"""
```

- Failure causes a short-circuit
- Returns an `Err` that tells you exactly what happened
- Can't ignore it
- Close to the origin where information is highest

---
### Simplifying Composition with `and_then`
```python
#: result.py
# Add and_then
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

ANSWER = TypeVar("ANSWER")
ERROR = TypeVar("ERROR")


@dataclass(frozen=True)
class Result(Generic[ANSWER, ERROR]):
    def and_then(
        self, func: Callable[[ANSWER], "Result"]
    ) -> "Result[ANSWER, ERROR]":
        if isinstance(self, Ok):
            return func(self.value)
        return self  # Pass the Err forward


@dataclass(frozen=True)
class Ok(Result[ANSWER, ERROR]):
    value: ANSWER

    def unwrap(self) -> ANSWER:
        return self.value


@dataclass(frozen=True)
class Err(Result[ANSWER, ERROR]):
    error: ERROR
```


---
```python
#: comprehension5.py
# Simplifying composition with and_then
from comprehension4 import func_a, func_b, func_c
from result import Result
from util import display
from validate_output import console


def composed(
    i: int,
) -> Result[str, str | ZeroDivisionError | ValueError]:
    # fmt: off
    return (
        func_a(i)
        .and_then(func_b)
        .and_then(func_c)
    )


if __name__ == "__main__":
    display(
        inputs := range(-1, 3),
        outputs := [composed(i) for i in inputs],
    )
    console == """
-1: Err(error=ValueError('func_c(-1)'))
0: Err(error=ZeroDivisionError('func_b(0)'))
1: Err(error='func_a(1)')
2: Ok(value='func_c(2)')
"""
```

---

### Handling Multiple Arguments

---
```python
#: multiple_arguments.py
from comprehension6 import func_a, func_b
from returns.result import Result
from util import display
from validate_output import console


def add(first: int, second: int) -> int:
    return first + second


def composed(
    i: int, j: int
) -> Result[int, str | ValueError]:
    # fmt: off
    return Result.do(
        add(first, second)
        for first in func_a(i)
        for second in func_b(j)
    )


display(
    inputs := [(1, 5), (7, 0), (2, 1)],
    outputs=[composed(*args) for args in inputs],
)
console == """
(1, 5): <Failure: func_a(1)>
(7, 0): <Failure: func_b(0)>
(2, 1): <Success: 3>
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
