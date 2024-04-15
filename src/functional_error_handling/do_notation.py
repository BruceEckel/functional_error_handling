#: do_notation.py
from returns.result import Result
from composed import a, b, c, composed
from test import test


# fmt: off
def do_notation(i: int):
    return Result.do(
        cr
        for ar in a(i)
        for br in b(ar)
        for cr in c(br)
    )

assert test(do_notation) == test(composed)
