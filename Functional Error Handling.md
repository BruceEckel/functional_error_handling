*This document, code examples, and presentation slides are in a [GitHub repository](https://github.com/BruceEckel/functional_error_handling)*.

<!-- #[code_location] ./src/functional_error_handling -->
> **Thesis**: *Most of what we've been working towards in programming—whether we are aware of it or not—is composability.* 

Discovering the meaning of composability is part of this path—there are different definitions depending on the programming language paradigm under scrutiny.
Here’s my definition:

> The ability to assemble bigger pieces from smaller pieces.

This is less-precise than some definitions. For example, composition in object-oriented programming means “putting objects inside other objects.” When dealing with functions, composability means “calling functions within other functions.” Both definitions fit my overall definition; they achieve the same goal but in different specific ways. 

To enable the easy construction of programs, we need to be able to effortlessly assemble components in the same way that a child assembles Legos—by simply sticking them together, without requiring extra activities. On top of that, such assemblages become their own components that can be stuck together just as easily. This composability scales up regardless of the size of the components.

Over the years we have encountered numerous roadblocks to this goal.
## Goto Considered Harmful

[Djikstra’s 1968 note](https://homepages.cwi.nl/~storm/teaching/reader/Dijkstra68.pdf) had quite an impact on the programming community, which at the time consisted largely of assembly-language programmers. For these, the goto statement was foundational, and denigrating it was a shock. Although he never explicitly mentioned functions in his note, the effect was to push programmers towards functions. [The creator of Structured Concurrency](https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/) provides a clear description of this.

Rather than jumping about within a limited program, functions restrict you to a single entry and single exit point, and this dramatically improves composability because you can no longer leave a section of code at any point using a goto (note that within a function scope you cannot know what’s outside that scope, thus you can’t jump somewhere because you don’t know a destination to jump to). 

My programming training was primarily as a computer engineer and I spent the first few years of my career programming in assembly. Assembly supports subroutine calls and returns, but not the loading of arguments on the stack and passing results back out—the programmer must write this error-prone code by hand.

Higher-level languages handle function arguments and returns for you, which made them a very desirable improvement as the size and complexity of programs grew beyond what the assembly programmer was able to hold in their head.
## Modules

Tim Peters’ observation of the value of namespaces (see [The Zen of Python](https://peps.python.org/pep-0020/)) is the core of the idea of modules, which more modern languages incorporate (unfortunately C++ had to inherit C’s messy system, for backwards compatibility). In Python, files are automatically modules, which is certainly one of the easiest solutions.

It wasn’t always this way. Breaking assembly-language programs into pieces was not easy, and early higher-level languages tended to be single-file programs and did not consider modularity. When the idea began to surface it was incorporated as a main feature of the Modula-2 language (a descendent of Pascal). The name tells you what a significant shift it was considered at the time.

Modula-2 and similar languages required an explicit declaration of a module:
```modula-2
MODULE Hello;
FROM STextIO IMPORT WriteString;
BEGIN
  WriteString("Hello World!")
END Hello.
```
This allowed complete granularity independent of file organization; perhaps this was because programmers were used to thinking in terms of one big file-per-program. Python’s merging of modules with files makes more sense in hindsight and has the benefit of eliminating the [(significant) extra verbiage](https://en.wikipedia.org/wiki/Modula-2), only a portion of which is shown here.

The main benefit of modules is name control—each module creates a scope for names (a namespace) which allows programmers the freedom to choose any name at will within a module. This prevents name collisions across a project and reduces the cognitive load on the programmer. Prior to this, programs reached scaling limits as they grew larger. Program size in assembly language programs was limited by many different factors, so the need for modules was not seen until systems were able to grow larger because higher-level languages solved enough of these other factors.

In modern languages, modularity is part of the background of a language and we don’t think much about it. At one time, however, the lack of modularity was a significant roadblock to code composability.
## Inheritance

Object-oriented programming has a bit of a tortured history. Although the first OO language was Simula-67 (a compiled language), OO found its first real success with Smalltalk. But Smalltalk might be the most dynamic language you’ll ever encounter—literally everything is evaluated at runtime. While this worked well for the kinds of problems Smalltalk was good at solving, it turned out that taking the ideas of Smalltalk and imprinting them into a statically-typed language lost a *lot* in translation.

# Error Handling

Error reporting and handling has been a significant impediment to composability.
## History

Original programs were small (by present-day standards), written in assembly language (machine code quickly became too unwieldy), and tightly coupled to the underlying hardware. If something went wrong, the only way to report it was to change the output on a wire, to turn on a light or a buzzer. If you had one, you put a message on the console—this might as simple as a dot-matrix display. Such an error message probably wasn’t friendly to the end-user of the system and usually required a tech support call to the manufacturer. 

Two of my first jobs were building embedded systems that controlled hardware. These systems had to work right. There was no point in reporting most errors because  an error normally meant the software was broken.

For business and scientific programming, Fortran and Cobol were batch processed on punch cards. If something went wrong, either the compilation failed or the resulting data was bad. No real-time error-handling was necessary because the program didn’t run in real time.

As time-sharing operating systems like Unix became a common way to distribute computing resources, program execution became more immediate. Users began to expect more interactive experiences, so programmers had to begin thinking about how to report and handle errors during the execution of a program, and in ideal cases recovering from those errors so the program could continue without shutting down.

Programmers produced a scattered collection of solutions to the reporting problem:

- Indicate failure by returning a special value from a function call. This only works when the special value doesn't occur from an ordinary call to that function. For example, if your function returns any `int`, you can't use `0` or `-1` to report an error. A bigger problem is that you rely on the client programmer to pay attention to the return value and know what to do about errors.
- Indicate failure by [setting a global flag](https://en.wikipedia.org/wiki/Errno.h). This is a single flag shared by all functions in the program. The client programmer must know to watch that flag. If the flag isn't checked right away, it might get overwritten by a different function call in which case the error is lost.
- Use [signals](https://en.wikipedia.org/wiki/C_signal_handling) if the operating system supports it.

The operating system was something that needed to be discovered. As programmers found themselves rewriting the same basic code over and over again, and much of that repeated code involved manipulating hardware and the attendant specialized knowledge required, it became clear that we needed a layer to eliminate this extra work, work that to some degree every program required.

A fundamental question that designers were trying to understand during this evolution was:

> *Who is responsible for error handling, the OS or the language?*

Since every program has the potential for errors, it initially seemed obvious that this activity should be the domain of the operating system. Some early operating systems allowed the program to invoke an error which would then jump to the operating system, and a few OSes even experimented with the ability to “resume” back to the point where the error occurred, so the handler could fix the problem and continue processing. Notably, these systems did not find success and resumption was removed. 

Further experiments eventually made it clear that the language needed primary responsibility for error reporting and handling (there are a few special cases, such as out-of-memory errors, which must still be handled by the OS). This is because an OS is designed to be general-purpose, and thus cannot know the specific situation that caused an error, whereas language code can be close to the problem. Customization is normally the domain of the language. You could imagine calling the OS to install custom error-handling routines, and you can also imagine how quickly that would become overwhelmingly messy.

If errors are in the language domain, the next question is how to report and handle them. 

# Exceptions

Unifying error reporting and recovery

Exceptions seemed like a great idea:
1. A standardized way to correct problems so that an operation can recover and retry
2. There's only one way to report errors
3. Errors cannot be ignored—they flow upward until caught or displayed on the console with program termination.
4. Errors can be handled close to the origin, or generalized by catching them "further out" so that multiple error sources can be managed with a single handler.
5. Exception hierarchies allow more general exception handlers to handle multiple exception subtypes

To be clear, exceptions were a big improvement over all of the previous (non) solutions to the error reporting problem. Exceptions moved us forward for awhile (and became entrenched in programming culture) until folks started discovering pain points. As is often the case, this happened as we tried to scale up to create larger and more complex systems. And once again, the underlying issue was composability.
## The Problem with Exceptions

In the small (and especially when teaching them), exceptions seem to work quite well. 

maybe you can't prove it, things work in the small but don't scale). We only figure it out when scaling composability.


### 1. The Two Kinds of Errors are Conflated
Recoverable vs panic
(Recovering/Retrying requires programming)
With exceptions, the two types are conflated.
(Link to Error handling article)
### 2. Exceptions are not Part of the Type System

You can’t know what exceptions you must handle when calling other functions (i.e.: composing).
Even if you track down all the possible exceptions thrown explicitly in the code (by hunting for them in their source code!), built-in exceptions can still happen without evidence in the code: divide-by-zero is a great example of this.

You can be using a library and handling all the exceptions from it (or perhaps just the ones you found in the documentation), and a newer version of that library can quietly add a new exception, and suddenly you are no longer detecting and/or handling all the exceptions. Even though you made no changes to your code.

If exceptions are part of the type system, you can know all the errors that can occur just by looking at the type information. If a library component adds a new error then that must be reflected in that component’s type signature, which means that the code using it immediately knows that it is no longer covering all the error conditions, and will produce type errors until it is fixed.

### 3. Exceptions Destroy Partial Calculations

Let’s start with a very simple example where we populate a `List` with the results of a sequence of calls to the function `f1`:

```python
#: comprehension1.py
# Exception produces no results, stops everything


def f1(i: int) -> int:
    if i == 1:
        raise ValueError("i cannot be 1")
    else:
        return i * 2


result = [f1(i) for i in range(3)]
print(result)
r"""
Traceback (most recent call last):
  ...
ValueError: i cannot be 1
"""
```

`f1` throws a `ValueError` exception if its argument is `1`. The `range(3)` is 0, 1, and 2; only one of these values causes the exception—`result` contains only one problem; the other two values are fine. However, we lose everything that we were calculating when the exception is thrown. This:
1. Is computationally wasteful, especially with large calculations.
2. Makes debugging harder. It would be quite valuable to see in `result` which parts succeeded and which parts failed.
# The Functional Solution
Instead of creating a complex implementation to report and handle errors, the functional approach creates a “return package” containing the answer along with the (potential) error information. Instead of only returning the answer, we return this package from the function. 

This package is a new type, with operations that prevent the programmer from simply plucking the result from the package without dealing with error conditions (a failing of the Go language approach).

As a first attempt, we can use *type unions* to create a nameless return package:

```python
#: comprehension2.py
# Type union aka Sum Type
# Success vs error is not clear
from validate_output import console


def f2(i: int) -> int | str:  # Sum type
    if i == 1:
        return "i cannot be 1"
    else:
        return i * 2


print(outputs := [f2(i) for i in range(3)])
console == """
[0, 'i cannot be 1', 4]
"""

for r in outputs:
    match r:
        case int(value):
            print(f"{value = }")
        case str(error):
            print(f"{error = }")
console == """
value = 0
error = 'i cannot be 1'
value = 4
"""


# Composition: return type enforced
def g(i: int) -> int | str:
    return f2(i)


print(g(1))
print(g(5))
console == """
i cannot be 1
10
"""
```
`console` is a tool in the GitHub repository that validates the correctness of the `console ==` strings. If you run the program you’ll see the same output as you see in the `console ==` strings.

`f2` returns a `str` to indicate an error, and an `int` answer if there is no error. In the pattern match, we are forced to check the result type to determine whether an error occurs and we cannot just assume it is an `int`.

An important problem with this approach is that it is not clear which type is the success value and which type represents the error condition—because we are trying to repurpose existing built-in types to represent new meanings.

In hindsight, it might seem like this “return package” approach is much more obvious than the elaborate exception-handling scheme that was adopted for C++, Java and other languages, but at the time the apparent overhead of returning extra bytes seemed unacceptable (I don’t know of any comparisons between that and the overhead of exception-handling mechanisms, but I do know that the goal of C++ exception handling is to have zero execution overhead if no exceptions occur).

Note that in the definition of `g`, the type checker requires that you return `int | str` because `f2` returns those types. Thus, when composing, type-safety is preserved. This means you won’t lose error type information during composition, so composability automatically scales.

## Unifying the Return Type

As you can see in the display of the `outputs` array, we now have the unfortunate situation that `outputs` contains multiple types (both `int` and `str`). The solution is to create a new type that unifies the “answer” and “error” types. We’ll call this `Result` and define it using generics to make it generally useful:

```python
#: result.py
# Result with OK & Err subtypes
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

ANSWER = TypeVar("ANSWER")
ERROR = TypeVar("ERROR")


@dataclass(frozen=True)
class Result(Generic[ANSWER, ERROR]):
    # Ignore this method for now:
    def and_then(self, func: Callable[[ANSWER], "Result"]) -> "Result[ANSWER, ERROR]":
        if isinstance(self, Ok):
            return func(self.value)
        return self  # Just pass the Err forward


@dataclass(frozen=True)
class Ok(Result[ANSWER, ERROR]):
    value: ANSWER  # Usage: return Ok(answer)

    def unwrap(self) -> ANSWER:
        return self.value


@dataclass(frozen=True)
class Err(Result[ANSWER, ERROR]):
    error: ERROR  # Usage: return Err(error)
```
(description)

The modified version of the example using `Result` is now:
```python
#: comprehension3.py
# Explicit result type
from result import Err, Ok, Result
from validate_output import console


def f3(i: int) -> Result[int, str]:
    if i == 1:
        return Err("i cannot be 1")
    else:
        return Ok(i * 2)


print(outputs := [f3(i) for i in range(3)])
console == """
[Ok(value=0), Err(error='i cannot be 1'), Ok(value=4)]
"""

for r in outputs:
    match r:
        case Ok(value):
            print(f"{value = }")
        case Err(error):
            print(f"{error = }")
console == """
value = 0
error = 'i cannot be 1'
value = 4
"""


# Composition: return type enforced
def g(i: int) -> Result[int, str]:
    return f3(i)


print(g(1))
print(g(5))
console == """
Err(error='i cannot be 1')
Ok(value=10)
"""
```

## Composing with Error Handling

```python
#: comprehension4.py
# Composing functions
from result import Err, Ok, Result
from validate_output import console


def a(i: int) -> Result[int, str]:
    if i == 1:
        return Err("i cannot be 1")
    else:
        return Ok(i)


# Use an exception as info (but don't raise it):
def b(i: int) -> Result[int, ZeroDivisionError]:
    if i == 0:
        return Err(ZeroDivisionError())
    return Ok(i)


def c(i: int) -> Result[str, ValueError]:
    if i == -1:
        return Err(ValueError(i))
    return Ok(f"{i}#")


def composed(i: int) -> Result[str, str | ZeroDivisionError | ValueError]:
    result_a = a(i)
    if isinstance(result_a, Err):
        return result_a

    result_b = b(result_a.unwrap())  # unwrap gets the value from Ok
    if isinstance(result_b, Err):
        return result_b

    result_c = c(result_b.unwrap())
    return result_c


inputs = range(-1, 3)
print(outputs := [composed(i) for i in inputs])
console == """
[Err(error=ValueError(-1)), Err(error=ZeroDivisionError()), Err(error='i cannot be 1'), Ok(value='2#')]
"""

for inp, outp in zip(inputs, outputs):
    print(f"{inp:>2}: {outp}")
console == """
-1: Err(error=ValueError(-1))
 0: Err(error=ZeroDivisionError())
 1: Err(error='i cannot be 1')
 2: Ok(value='2#')
"""
```

## Simplifying Composition with `and_then`

```python
#: comprehension5.py
# Simplifying composition with and_then
from result import Err, Ok, Result
from validate_output import console
from comprehension4 import a, b, c


def composed(i: int) -> Result[str, str | ZeroDivisionError | ValueError]:
    return a(i).and_then(b).and_then(c)


inputs = range(-1, 3)
print(outputs := [composed(i) for i in inputs])
console == """
[Err(error=ValueError(-1)), Err(error=ZeroDivisionError()), Err(error='i cannot be 1'), Ok(value='2#')]
"""

for inp, outp in zip(inputs, outputs):
    print(f"{inp:>2}: {outp}")
console == """
-1: Err(error=ValueError(-1))
 0: Err(error=ZeroDivisionError())
 1: Err(error='i cannot be 1')
 2: Ok(value='2#')
"""
```
## A More Capable Library

Although `result.py` creates typed “answer + error” packages, there’s still a problem that impedes our ultimate goal of composability: every time you call a function, you must write code to unpack and deal with this new `Result` object. This is not only a lot of extra repetitive work, but it interrupts the flow and readability of the program. We need some way to reduce or eliminate this extra code.

Languages like Rust and Kotlin support these unpacking operations directly (examples):

Languages like Python do not directly support this unpacking, but the mathematical field of *category theory* proves that operations can be created to automatically stop a composed calculation if an error occurs, returning the error from the composition. These operations have multiple names such as *bind* and *flatmap*.

The most popular Python library that includes this extra functionality is [Returns](https://github.com/dry-python/returns), which provides `bind`. `Returns` includes more features than just return package support, but we will only focus on that.

`Returns` elegantly solves the list-comprehension problem:
```python
#: comprehension6.py
# Using https://github.com/dry-python/returns
from returns.pipeline import is_successful, pipe
from returns.pointfree import bind
from returns.result import Failure, Result, Success, safe
from validate_output import console


def a(i: int) -> Result[int, str]:
    if i == 1:
        return Failure(f"a({i = })")
    return Success(i)


# Convert existing function.
# Return type becomes Result[int, ZeroDivisionError]
@safe
def b(i: int) -> int:
    print(f"b({i}): {1 / i}")
    return i


def c(i: int) -> Result[str, ValueError]:
    if i == -1:
        return Failure(ValueError(f"c({i =})"))
    return Success(f"c({i})")


composed = pipe(  # type: ignore
    a,
    bind(b),
    bind(c),
)

inputs = range(-1, 3)  # [-1, 0, 1, 2]
outputs = [composed(i) for i in inputs]
console == """
b(-1): -1.0
b(2): 0.5
"""

for inp, outp in zip(inputs, outputs):
    print(f"{inp:>2}: {outp}")
console == """
-1: <Failure: c(i =-1)>
 0: <Failure: division by zero>
 1: <Failure: a(i = 1)>
 2: <Success: c(2)>
"""

# Extract results, converting failure to None:
with_nones = [r.value_or(None) for r in outputs]
print(str(with_nones))
print(str(list(filter(None, with_nones))))
console == """
[None, None, None, 'c(2)']
['c(2)']
"""

# Another way to extract results:
for r in outputs:
    if is_successful(r):
        print(f"{r.unwrap() = }")
    else:
        print(f"{r.failure() = }")
console == """
r.failure() = ValueError('c(i =-1)')
r.failure() = ZeroDivisionError('division by zero')
r.failure() = 'a(i = 1)'
r.unwrap() = 'c(2)'
"""
```

## Handling Multiple Arguments

```python
#: multiple_arguments.py
from returns.result import Failure, Result, Success
from validate_output import console


def not_one(i: int) -> Result[int, ValueError]:
    if i == 1:
        return Failure(ValueError(f"not_one: {i = }"))
    return Success(i * 10)


def not_two(j: int) -> Result[int, ValueError]:
    if j == 2:
        return Failure(ValueError(f"not_two: {j = }"))
    return Success(j * 100)


def add(first: int, second: int) -> int:
    return first + second


def do_add(i: int, j: int) -> Result[int, ValueError]:
    # fmt: off
    return Result.do(
        add(first, second) 
        for first in not_one(i) 
        for second in not_two(j)
    )


inputs = [(1, 5), (7, 2), (3, 4)]
outputs = [do_add(*inp) for inp in inputs]
for inp, outp in zip(inputs, outputs):
    print(f"{inp}: {outp}")
console == """
(1, 5): <Failure: not_one: i = 1>
(7, 2): <Failure: not_two: j = 2>
(3, 4): <Success: 430>
"""
```
