# Functional Error Handling
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

**`comprehension1.py`**

---
### The Functional Approach

- Stop using exceptions
- Functions return a “package” combining the answer + potential error
- We can do this with a *type union*:

**`comprehension2.py`**

---
### Create a new Type for Returns

**`result.py`**

### Incorporate `Result`

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

Let's add a new method `and_then` to `Result`:

**`result.py`**

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
