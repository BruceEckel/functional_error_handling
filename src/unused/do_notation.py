#: do_notation.py
# Alternative to flow/bind
from test import test

from comprehension5 import composed, reject_0, reject_1, reject_minus_1
from returns.result import Result


# fmt: off
def do_notation(i: int):
    return Result.do(
        c_result
        for a_result in reject_1(i)
        for b_result in reject_0(a_result)
        for c_result in reject_minus_1(b_result)
    )

assert test(do_notation) == test(composed)
