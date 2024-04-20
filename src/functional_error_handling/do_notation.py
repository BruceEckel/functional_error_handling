#: do_notation.py
# Alternative to flow/bind
from returns.result import Result
from composed import a, b, c, composed
from test import test


# fmt: off
def do_notation(i: int):
    return Result.do(
        c_result
        for a_result in a(i)
        for b_result in b(a_result)
        for c_result in c(b_result)
    )

assert test(do_notation) == test(composed)
