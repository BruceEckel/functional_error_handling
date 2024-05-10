# Functional Error Handling

*This document, code examples, and presentation slides are in a [GitHub repository](https://github.com/BruceEckel/functional_error_handling)*. 
This paper assumes full usage of Python’s type system.

---

# Thesis

> *Most of what we've been working towards in programming—whether we are aware of it or not—is composability.* 

My definition:

> The ability to assemble bigger pieces from smaller pieces.

> To effortlessly assemble components in the same way that a child assembles Legos.

---

# Roadblock: Goto Considered Harmful

Pushed programmers towards functions.

Functions present the caller with a single entry and exit point.

---

# Modules

Lack of namespace control was a significant roadblock to composability

Python files are automatically modules

---
# Inheritance

Inheritance breaks encapsulation

This impedes composability

---

# Error Handling

A significant impediment to composability.

Numerous attempts, usually global solutions with race conditions

Is it in the domain of the OS or the language?

---

# Exceptions

Standardized error handling in the language domain. 

Unifies error reporting and recovery.

Errors can't be ignored.


---

## Problems with Exceptions

In the small (and especially when teaching them), exceptions seem to work quite well. 

---

### 1. The Two Kinds of Errors are Conflated

Recoverable vs panic

---

### 2. Exceptions are not Part of the Type System

Caller can’t know what exceptions might emerge.

Even if you figure them all out, the function can start throwing a new kind of exception.

C++ and Java tried *exception specifications* which didn't work.

When errors are included in the type system, all errors are type-checked.


---

### 3. Exception Specifications Create a “Shadow Type System”

Languages like C++ and Java attempted to add notation indicating the exceptions that might emerge from a function call. This was well-intentioned and seems to produce the necessary information the client programmer needs to handle errors. The fundamental problem was that this created an alternate or “shadow” type system that doesn’t follow the same rules as the primary type system. To make the shadow type system work, its rules were warped to the point where it became effectively useless (a discovery that has taken years to realize).

C++ exception specifications were originally optional and not statically type-checked. After many years these were deprecated in favor of the statically-typed [`expected` specification](https://en.cppreference.com/w/cpp/utility/expected) (which takes the functional approached described in this paper). 

Java created checked exceptions, which must be explicitly dealt with in your code, and runtime exceptions, which could be ignored. Eventually they added a feature that allows checked exceptions to be easily converted into runtime exceptions. Java functions can always return `null` without any warning.

Both systems (the original C++ dynamic exception specifications, and Java exception specifications) had too many holes, and it was too difficult to effectively support both the main and shadow type systems.

---

### 4. Exceptions Destroy Partial Calculations

Let’s start with a very simple example where we populate a `List` with the results of a sequence of calls to the function `reject_1`:

```python

---

#: comprehension1.py

---

# Exception produces no results, stops everything


def reject_1(i: int) -> int:
    if i == 1:
        raise ValueError("i is 1")
    return i * 2


result = [reject_1(i) for i in range(3)]
print(result)
"""
Traceback (most recent call last):
  ...
ValueError: i is 1
"""
```

`reject_1` throws a `ValueError` if its argument is `1`. The `range(3)` is 0, 1, and 2; only one of these values causes the exception. So `result` contains only one problem; the other two values are fine. However, we lose everything that we were calculating when the exception is thrown. This:
1. Is computationally wasteful, especially with large calculations.
2. Makes debugging harder. It would be quite valuable to see in `result` the parts that succeeded and those that failed.

---

# The Functional Solution
Instead of creating a complex implementation to report and handle errors, the functional approach creates a “return package” containing the answer along with the (potential) error information. Instead of only returning the answer, we return this package from the function. 

This package is a new type, with operations that prevent the programmer from simply plucking the result from the package without dealing with error conditions (a failing of the Go language approach).

A first attempt uses *type unions* to create a nameless return package:

```python

---

#: comprehension2.py

---

# Type union aka Sum Type

---

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



---

# Return type enforced
def composed(i: int) -> int | str:
    return reject_1(i)


print(composed(1))
print(composed(5))
console == """
i is 1
10
"""
```

`validate_output` is a tool in the [GitHub repository](https://github.com/BruceEckel/functional_error_handling) that validates the correctness of the `console ==` strings. If you run the program you’ll see the same output as you see in the `console ==` strings.

`reject_1` returns a `str` to indicate an error, and an `int` answer if there is no error. In the pattern match, we are forced to check the result type to determine whether an error occurs; we cannot just assume it is an `int`.

An important problem with this approach is that it is not clear which type is the success value and which type represents the error condition—because we are trying to repurpose existing built-in types to represent new meanings.

In hindsight, it might seem like this “return package” approach is much more obvious than the elaborate exception-handling scheme that was adopted for C++, Java and other languages, but at the time the apparent overhead of returning extra bytes seemed unacceptable (I don’t know of any comparisons between that and the overhead of exception-handling mechanisms, but I do know that the goal of C++ exception handling is to have zero execution overhead if no exceptions occur).

Note that in the definition of `composed`, the type checker requires that you return `int | str` because `reject_1` returns those types. Thus, when composing, type-safety is preserved. This means you won’t lose error type information during composition, so composability automatically scales.

---

## Unifying the Return Type

We now have the unfortunate situation that `outputs` contains multiple types: both `int` and `str`. The solution is to create a new type that unifies the “answer” and “error” types. We’ll call this `Result` and define it using generics to make it universally applicable:

```python

---

#: result.py

---

# Result with OK & Err subtypes
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

ANSWER = TypeVar("ANSWER")
ERROR = TypeVar("ERROR")


@dataclass(frozen=True)
class Result(Generic[ANSWER, ERROR]):
    # Ignore this method for now:
    def and_then(
        self, func: Callable[[ANSWER], "Result"]
    ) -> "Result[ANSWER, ERROR]":
        if isinstance(self, Ok):
            return func(self.value)
        return self  # Pass the Err forward


@dataclass(frozen=True)
class Ok(Result[ANSWER, ERROR]):
    value: ANSWER  # Usage: return Ok(answer)

    def unwrap(self) -> ANSWER:
        return self.value


@dataclass(frozen=True)
class Err(Result[ANSWER, ERROR]):
    error: ERROR  # Usage: return Err(error)
```

A `TypeVar` defines a generic parameter. We want `Result` to contain a type for an `ANSWER` when the function call is successful, and an `ERROR` to indicate how the function call failed. Each subtype of `Result` only holds one field: `value` for a successful `Ok` calculation, and `error` for a failure (`Err`). Thus, if an `Err` is returned, the client programmer cannot simply reach in and grab the `value` field because it doesn’t exist. The client programmer is forced to properly analyze the `Result`.

To use `Result`, you `return Ok(answer)` when you’ve successfully created an answer, and `return Err(error)` to indicate a failure. `unwrap` is a convenience method which is only available for an `Ok` (we’ll look at `and_then` later).

The modified version of the example using `Result` is now:

```python

---

#: comprehension3.py

---

# Explicit result type
from result import Err, Ok, Result
from validate_output import console


def reject_1(i: int) -> Result[int, str]:
    if i == 1:
        return Err("i is 1")
    return Ok(i * 2)


print(outputs := [reject_1(i) for i in range(3)])
console == """
[Ok(value=0), Err(error='i is 1'), Ok(value=4)]
"""

for r in outputs:
    match r:
        case Ok(value):
            print(f"{value = }")
        case Err(error):
            print(f"{error = }")
console == """
value = 0
error = 'i is 1'
value = 4
"""


def composed(i: int) -> Result[int, str]:
    return reject_1(i)


print(composed(1))
print(composed(5))
console == """
Err(error='i is 1')
Ok(value=10)
"""
```

Now `reject_1` returns a single type, `Result`. The first type parameter to `Result` is the type returned by `Ok` and the second type parameter is the type returned by `Err`. The `outputs` from the comprehension are all of type `Result`, and we have preserved the successful calculations even though there is a failing call. We can also pattern-match on the outputs, and it is crystal-clear which match is for the success and which is for the failure.

---

## Composing with `Result`

The previous examples included very simple composition in the `compsed` functions which just called a single other function. What if you need to compose a more complex function from multiple other functions? The `Result` type ensures that the `composed` function properly represents both the `Answer` type but also the various different errors that can occur:

```python

---

#: comprehension4.py

---

# Composing functions
from result import Err, Ok, Result
from util import display
from validate_output import console


def reject_1(i: int) -> Result[int, str]:
    if i == 1:
        return Err("i is 1")
    return Ok(i)



---

# Use an exception as info (but don't raise it):
def reject_0(i: int) -> Result[int, ZeroDivisionError]:
    if i == 0:
        return Err(ZeroDivisionError())
    return Ok(i)


def reject_minus_1(i: int) -> Result[str, ValueError]:
    if i == -1:
        return Err(ValueError(i))
    return Ok(f"{i}#")


def composed(
    i: int,
) -> Result[str, str | ZeroDivisionError | ValueError]:
    result_a = reject_1(i)
    if isinstance(result_a, Err):
        return result_a

    result_b = reject_0(
        result_a.unwrap()  # unwrap gets the value from Ok
    )
    if isinstance(result_b, Err):
        return result_b

    result_c = reject_minus_1(result_b.unwrap())
    return result_c


if __name__ == "__main__":
    display(inputs := range(-1, 3), [composed(i) for i in inputs])
    console == """
-1: Err(error=ValueError(-1))
0: Err(error=ZeroDivisionError())
1: Err(error='i is 1')
2: Ok(value='2#')
"""
```

The `a`, `b` and `c` functions each have argument values that are unacceptable. Notice that `b` and `c` both use built-in exception types as arguments to `Err`, but those exceptions are never raised—they are simply used to convey information, just like the `str` in `a`.

In `composed`, we call `a`, `b` and `c` in sequence. After each call, we check to see if the result type is `Err`. If so, the calculation has failed and we can’t continue, so we return the current result, which is an `Err` object containing the reason for the failure. If it succeeds, it is an `Ok` which contains an `unwrap` method that is used to extract the answer from that calculation—if you look back at `Result`, you’ll see that it returns the `ANSWER` type so its use can be properly type-checked.

This means that any failure during a sequence of composed function calls will short-circuit out of `composed`, returning an `Err` that tells you exactly what happened, and that you must decide what to do with. You can’t just ignore it and assume that it will “bubble up” until it finds an appropriate handler. You are forced to deal with it at the point of origin, which is typically when you know the most about an error.

---

## Simplifying Composition with `and_then`

There’s still a problem that impedes our ultimate goal of composability: every time you call a function within a composed function, you must write code to check the `Result` type and extract the success value with `unwrap`. This is extra repetitive work that interrupts the flow and readability of the program. We need some way to reduce or eliminate the extra code.

The `and_then` method in `Result` (see the comment in `result.py` that said “Ignore this method for now”) solves this exact problem:

```python

---

#: comprehension5.py

---

# Simplifying composition with and_then
from comprehension4 import reject_0, reject_1, reject_minus_1
from result import Result
from util import display
from validate_output import console


def composed(
    i: int,
) -> Result[str, str | ZeroDivisionError | ValueError]:
    return reject_1(i).and_then(reject_0).and_then(reject_minus_1)


display(inputs := range(-1, 3), [composed(i) for i in inputs])
console == """
-1: Err(error=ValueError(-1))
0: Err(error=ZeroDivisionError())
1: Err(error='i is 1')
2: Ok(value='2#')
"""
```

In `composed`, we call `a(i)` which returns a `Result`. The `and_then` method is called on that `Result`, passing it the next function we want to call (`b`) as an argument. The return value of `and_then` is *also* a `Result`, so we can call `and_then` again upon that `Result`, passing it the third function we want to call (`c`).

To understand what’s happening, here’s the definition of `and_then` taken from `result.py`:

```python
    def and_then(
        self, func: Callable[[ANSWER], "Result"]
    ) -> "Result[ANSWER, ERROR]":
        if isinstance(self, Ok):
            return func(self.value)
        return self  # Pass the Err forward
```

At each “chaining point” in `reject_1(i).and_then(reject_0).and_then(reject_minus_1)`, `and_then` checks to see if the previous call was successful. If so, it passes the result `value` from that call as the argument to the next function in the chain. If not, that means `self` is an `Err` object (containing specific error information), so all it needs to do is `return self`. The next call in the chain sees that the returned type is `Err`, so it doesn’t try to apply the next function but just (again) returns the `Err`. Once you produce an `Err`, no more function calls occur (that is, it short-circuits) and the `Err` result gets passed all the way out of the composed function so the caller can deal with the specific failure.

---

## A More Capable Library

We could continue adding features to our `Result` library until it becomes a complete solution. However, others have worked on this problem so it makes more sense to reuse their libraries. The most popular Python library that includes this extra functionality is [Returns](https://github.com/dry-python/returns). `Returns` includes other features, but we will only focus on  `Result`.

`Returns` provides elegant composition using *pipes* and the `bind` function:

```python

---

#: comprehension6.py

---

# Using https://github.com/dry-python/returns
from returns.pipeline import is_successful, pipe
from returns.pointfree import bind
from returns.result import Failure, Result, Success, safe
from util import display
from validate_output import console


def reject_1(i: int) -> Result[int, str]:
    if i == 1:
        return Failure(f"reject_1({i = })")
    return Success(i)



---

# Convert existing function.

---

# Return type becomes Result[int, ZeroDivisionError]
@safe
def reject_0(i: int) -> int:
    print(f"reject_0({i}) succeeded: {1 / i}")
    return i


def reject_minus_1(i: int) -> Result[str, ValueError]:
    if i == -1:
        return Failure(ValueError(f"c({i =})"))
    return Success(f"reject_minus_1({i})")


composed = pipe(  # type: ignore
    reject_1,
    bind(reject_0),
    bind(reject_minus_1),
)

inputs = range(-1, 3)  # [-1, 0, 1, 2]
outputs = [composed(i) for i in inputs]
console == """
reject_0(-1) succeeded: -1.0
reject_0(2) succeeded: 0.5
"""

display(inputs, outputs)
console == """
-1: <Failure: c(i =-1)>
0: <Failure: division by zero>
1: <Failure: reject_1(i = 1)>
2: <Success: reject_minus_1(2)>
"""


---

# Extract results, converting failure to None:
with_nones = [r.value_or(None) for r in outputs]
print(str(with_nones))
print(str(list(filter(None, with_nones))))
console == """
[None, None, None, 'reject_minus_1(2)']
['reject_minus_1(2)']
"""


---

# Another way to extract results:
for r in outputs:
    if is_successful(r):
        print(f"{r.unwrap() = }")
    else:
        print(f"{r.failure() = }")
console == """
r.failure() = ValueError('c(i =-1)')
r.failure() = ZeroDivisionError('division by zero')
r.failure() = 'reject_1(i = 1)'
r.unwrap() = 'reject_minus_1(2)'
"""
```

The definition of `reject_1` looks the same as previous versions, except that we now return `Failure` instead of `Err` and `Success` instead of ‘Ok’.

`Returns` provides a `@safe` decorator that you see applied to the “plain” function `reject_0`. This changes the normal `int` return type into a `Result` that includes `int` for the `Success` type but is also somehow able to recognize that the division might produce a `ZeroDivisionError` and include that in the `Failure` type. In addition, `@safe` is apparently catching the exception and converting it to the `ZeroDivisionError` returned as the information object in the `Failure` object. `@safe` is a helpful tool when converting exception-throwing code into error-returning code.

`reject_minus_1` adds some variety by rejecting `-1` and producing a `str` result. We can now produce `composed` using a `pipe` and `bind`. All the previous error-checking and short-circuiting behaviors happen as before, but the syntax is now more straightforward and readable.

Notice that when the `outputs` list is created, the output from `reject0` only happens for the values `-1` and `2`, because the other values cause errors in the `composed` chain of operations. The value `1` never gets to `reject_0` because it is intercepted by the prior `composed` call to `reject_1`. The value `0` causes `reject_0` to produce a `ZeroDivisionError` when it tries to perform the division inside the `print`.

[Explain rest of example]

Note that there may be an issue with the `Returns` library, which is that for proper type checking it requires using a MyPy extension. So far I have been unable to get that extension to work (however, I have no experience with MyPy extensions).

---

## Handling Multiple Arguments

The `pipe` is limiting because it assumes a single argument. What if you need to create a `composed` function that takes multiple arguments? For this, we use something called “do notation,” which you access using `Result.do`:

```python

---

#: multiple_arguments.py
from returns.result import Failure, Result, Success
from util import display
from validate_output import console


def reject_1(i: int) -> Result[int, ValueError]:
    if i == 1:
        return Failure(ValueError(f"not_one: {i = }"))
    return Success(i * 10)


def reject_2(j: int) -> Result[int, ValueError]:
    if j == 2:
        return Failure(ValueError(f"not_two: {j = }"))
    return Success(j * 100)



---

# Ordinary function:
def add(first: int, second: int) -> int:
    return first + second


def composed(i: int, j: int) -> Result[int, ValueError]:
    # fmt: off
    return Result.do(
        add(first, second)
        for first in reject_1(i)
        for second in reject_2(j)
    )


inputs = [(1, 5), (7, 2), (3, 4)]
outputs = [composed(*args) for args in inputs]
display(inputs, outputs)
console == """
(1, 5): <Failure: not_one: i = 1>
(7, 2): <Failure: not_two: j = 2>
(3, 4): <Success: 430>
"""
```



---

# Functional Error Handling is Happening

Functional error handling has already appeared in languages like Rust, Kotlin, and recent versions of C++ support these combined answer-error result types, with associated unpacking operations. In these languages, errors become part of the type system and it is far more difficult for an error to “slip through the cracks.”

Python has only been able to support functional error handling since the advent of typing and type checkers, and it doesn’t provide any direct language or library constructs for this. The benefits of better error handling and robust composability make it worth adopting a library like `Results`.


---

#### Acknowledgements

Most of the understanding I needed to explain this topic came from my attempts to help on the book by Bill Frasure and James Ward, probably titled “Effect-Oriented Programming,” that we’ve been working on for over three years. I’ve also learned a lot from some of the interviews that James and I have done for the [Happy Path Programming podcast](https://happypathprogramming.com/).

Despite its unreliability, I have found ChatGPT exceptionally useful for speeding up and improving my programming.
