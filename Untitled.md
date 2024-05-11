# Presentations using Slides

A demo on how to build presentations using Slides.
Is the next line merged?

---

## Formatting

You can use regular Markdown formatting, like *emphasized* and **bold** text.

1. bullet one
2. bullet two
3. Bullet three

Actual bullets
- abcde
- fghijk
- lmnopq


---

```python
#: comprehension5.py

def composed(
    i: int,
) -> Result[str, str | ZeroDivisionError | ValueError]:
    return func_a(i).and_then(func_b).and_then(func_c)

display(inputs := range(-1, 3), [composed(i) for i in inputs])
console == """
-1: Err(error=ValueError(-1))
0: Err(error=ZeroDivisionError())
1: Err(error='i is 1')
2: Ok(value='2#')
"""
```
