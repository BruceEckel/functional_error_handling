# Functional Error Handling
Bruce Eckel
Github: BruceEckel/functional_error_handling

---

- Github: BruceEckel/functional_error_handling
    - These slides (Slides.md for Obsidian)
    - Paper that goes in depth
    - Code examples + tools

- Requires Python type annotations + checker

---
#### Acknowledgements

- My attempts to help Bill Frasure & James Ward
- Book: “Effect-Oriented Programming”
- Interviews that James and I have done for the [Happy Path Programming podcast](https://happypathprogramming.com/).
- ChatGPT: Unreliable but still very useful

---

- Most of what we've been working towards in programming—whether we are aware of it or not—is composability

> The ability to assemble bigger pieces from smaller pieces

- Effortlessly assemble components in the same way a child assembles Legos

---

### Goto Considered Harmful

- Djikstra’s 1968 note pushed programmers towards functions

- Functions present the caller with a single entry and exit point

---

### No Namespace Control

- Modules isolate namespaces

- Python files are automatically modules

---
### Inheritance

- Breaks encapsulation --> impedes composability

---
### Error Handling

- Different approaches made it hard to compose
- Usually global solutions with race conditions
- The domain of the OS or the language?

---
### Exceptions

- In the language domain: closer to the problem
- Standard way to report errors
- Unifies error reporting and recovery
- Errors can't be ignored

---
- In the small, exceptions seem to work well
- Scaling up (composing) reveals problems

---
### 1. Conflates Categories

- Recoverable
- Panic: program can't continue
    - Treated the same as recoverable
    - Unecessary overhead
---
### 2. Not Part of the Type System

- Don’t know what exceptions will emerge
- The function can start throwing new ones
- C++ and Java tried *exception specifications*—didn't work
- We need error-handling enforced through types

---
### 3. Exception Specifications Create a “Shadow Type System”

---
### 4. Exceptions Destroy Partial Calculations

1. Computationally wasteful, especially with large calculations
2. Makes debugging harder

**`comprehension1.py`**

---
### The Functional Solution

- Stop using exceptions
- Return a “package” containing the answer + potential error
- *Type union* creates a nameless return package:

**`comprehension2.py`**

---
### Create a new Type for Returns

**`result.py`**

---
### Incorporating `Result`

**`comprehension3.py`**

---
### Composing with `Result`

**`comprehension4.py`**

- Failure causes a short-circuit
- Returns an `Err` that tells you exactly what happened
- Can't ignore it
- Close to the origin where information is highest

---
### Simplifying Composition with `and_then`

**`comprehension5.py`**

---
### A More Capable Library

**`comprehension6.py`**

---
### Handling Multiple Arguments

**`multiple_arguments.py`**

---
### Functional Error Handling is Happening

- Already in Rust, Kotlin, and recent versions of C++
- Errors are part of the type system
- Far more difficult for an error to slip through the cracks
- Benefits make it worth adopting a library like `Results`

---
- Open spaces session if you want to Q&A
