#: do_notation.py
# Alternative to flow/bind
from test import test

from example5 import composed, func_a, func_b, func_c
from returns.result import Result


# fmt: off
def do_notation(i: int):
    return Result.do(
        c_result
        for a_result in func_a(i)
        for b_result in func_b(a_result)
        for c_result in func_c(b_result)
    )

assert test(do_notation) == test(composed)
