# Functional Error Handling
Bruce Eckel
Github: BruceEckel/functional_error_handling

---

- Github: BruceEckel/functional_error_handling
    - Code examples + tools
    - Paper (in progress): for depth in things I can only touch on
    - These slides

- Requires Python type annotations + checker

---
#### Acknowledgements

- Helping Bill Frasure & James Ward on
> Effect-Oriented Programming
- People James and I have interviewed for the [Happy Path Programming podcast](https://happypathprogramming.com/).
- ChatGPT: Unreliable but still very useful

---
#### Thesis
- Most of what we've been working towards in programming—whether we are aware of it or not—is composability

> Combining smaller pieces into bigger pieces

- Effortlessly assemble components in the same way a child assembles Legos

---
### Impediments to Composability
- Gotos -> Functions
- The Need for Modules
- Inheritance Breaks Encapsulation
- Error Handling

---
### Error Handling

- Messy history with different approaches
- Usually: global solutions with race conditions
- Hard to compose
- The domain of the OS or the language?
    - Initial OS experiments, including resumption

---
### Exceptions

- Language domain is closer to the problem
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
- C++ and Java tried a shadow type system: *exception specifications*—didn't work

---
### 2. Conflates Categories

1. Recoverable
2. Panic: program can't continue
    - Treated the same as recoverable
    - Unecessary overhead

---
### 3. Exceptions Destroy Partial Calculations

- Computationally wasteful, especially with large calculations
- Makes debugging harder

**`example1.py`**

---
### The Functional Approach

- Stop using exceptions
- Functions return a structure combining the answer + potential error
- We can do this with a *type union*:

**`example2.py`**

---
### A new Return Type

**`result.py`**

### Incorporate `Result`

**`example3.py`**

---
### Composing with `Result`

**`example4.py`**

- Failure causes a short-circuit
- Returns a `Failure` that tells you exactly what happened
- Can't ignore it
- Close to the origin where information is highest

---
### Simplifying Composition with `bind`

Let's add a new method `bind` to `Result`:

**`result_with_bind.py`**

**`example5.py`**

---
### Handling Multiple Arguments

**`example6.py`**

---
### Functional Error Handling is Happening

- Already in Rust, Kotlin, and recent versions of C++
- Errors are part of the type system
- Far more difficult for an error to slip through the cracks
- Benefits make it worth adopting a library like `Results`

---
- Open spaces session for Q&A & Discussion:  Today (Saturday) 1pm Room 318
- Meet for dinner tonight 6:15 Westin Lobby
