# Presentations using Slides

A demo on how to build presentations using Slides.

---

## Formatting

You can use regular Markdown formatting, like *emphasized* and **bold** text.


---

```python


#: comprehension5.py

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