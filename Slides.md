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

- Djikstra pushed programmers towards functions

- Functions present the caller with a single entry and exit point

---

### Modules

- Lack of namespace control: a significant roadblock

- Python files are automatically modules

---
### Inheritance

- Impedes composability because it breaks encapsulation

---
### Error Handling

- Different approaches made it hard to compose
- Numerous attempts, usually global solutions with race conditions
- The domain of the OS or the language?

---
### Exceptions

- Standardized error handling 
- In the language domain
- Unifies error reporting and recovery
- Errors can't be ignored

---
- In the small, exceptions seem to work well
- Scaling up reveals problems

---
### 1. Conflates the Two Kinds of Errors

- Panic
- Recoverable

---
### 2. Not Part of the Type System

- Caller can’t know what exceptions might emerge

- If you figure them out, the function can start throwing new ones

- C++ and Java tried *exception specifications*—didn't work

- When errors are included in the type system, all errors are type-checked

---
### 3. Exception Specifications Create a “Shadow Type System”

- Error specification types vs. language types

---
### 4. Exceptions Destroy Partial Calculations

**`comprehension1.py`**

1. Computationally wasteful, especially with large calculations
2. Makes debugging harder

---
### The Functional Solution

- Create a “return package” containing the answer + potential error
- *Type union* creates a nameless return package:

**`comprehension2.py`**

---
### Unifying the Return Type

**`result.py`**

---
### Incorporating `Result`

**`comprehension3.py`**

---
### Composing with `Result`

**`comprehension4.py`**

- Failure short-circuits
- Returns an `Err` that tells you exactly what happened
- Can't ignore it
- Close to the origin where information is highest

---
### Simplifying Composition with `and_then`

**`comprehension5.py`**

```python
    def and_then(
        self, func: Callable[[ANSWER], "Result"]
    ) -> "Result[ANSWER, ERROR]":
        if isinstance(self, Ok):
            return func(self.value)
        return self  # Pass the Err forward
```

---
### A More Capable Library

**`comprehension6.py`**

---
### Handling Multiple Arguments

**`multiple_arguments.py`**

---
### Functional Error Handling is Happening

- Already appears in Rust, Kotlin, and recent versions of C++
- Errors are part of the type system
- Far more difficult for an error to “slip through the cracks”
- Benefits make it worth adopting a library like `Results`
