# Functional Error Handling
Bruce Eckel

---

- https://github.com/BruceEckel/functional_error_handling
    - This document
    - Code examples
    - Presentation slides

- Requires Python type annotations

---

- Most of what we've been working towards in programming—whether we are aware of it or not—is composability

> The ability to assemble bigger pieces from smaller pieces

- To effortlessly assemble components in the same way a child assembles Legos

---

### Goto Considered Harmful

- Djikstra pushed programmers towards functions

- Functions present the caller with a single entry and exit point

---

### Modules

- Lack of namespace control: a significant composability roadblock

- Python files are automatically modules

---
### Inheritance

- Breaks encapsulation

- Impedes composability

---

### Error Handling

- Significant impediment to composability

- Numerous attempts, usually global solutions with race conditions

- In the domain of the OS or the language?

---

### Exceptions

- Standardized error handling in the language domain

- Unifies error reporting and recovery

- Errors can't be ignored

---

### Problems with Exceptions

- In the small (and especially when teaching them), exceptions seem to work quite well

---

### 1. Conflates the Two Kinds of Errors

- Recoverable vs panic

---

### 2. Not Part of the Type System

- Caller can’t know what exceptions might emerge

- If you figure them out, the function can start throwing new ones

- C++ and Java tried *exception specifications*; didn't work

- When errors are included in the type system, all errors are type-checked

---

### 3. Exception Specifications Create a “Shadow Type System”

- The error specification type system
- The language type system
- Often don't cover the same ground

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

- Failure during a sequence of composed function calls short-circuits out
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

- Has already appeared in languages like Rust, Kotlin, and recent versions of C++
- Errors become part of the type system
- Far more difficult for an error to “slip through the cracks”
- Benefits make it worth adopting a library like `Results`

---

#### Acknowledgements

Most of the understanding I needed to explain this topic came from my attempts to help on the book by Bill Frasure and James Ward, probably titled “Effect-Oriented Programming,” that we’ve been working on for over three years. I’ve also learned a lot from some of the interviews that James and I have done for the [Happy Path Programming podcast](https://happypathprogramming.com/).

Despite its unreliability, I have found ChatGPT exceptionally useful for speeding up and improving my programming.
