#: composed_tuples.py
# Multiple arguments within composed function using tuples
from returns.result import Result, Success, Failure
from returns.pipeline import flow
from returns.pointfree import bind
from validate_output import console
from typing import Tuple


def first(t: Tuple[int, int]) -> Result[Tuple[int, int], str]:
    i, j = t
    # print(f"first {i = }, {j = }")
    if i == j:
        return Failure(f"first({i = }, {j = })")
    return Success((i, j))


def second(t: Tuple[int, int]) -> Result[int, str]:
    u, v = t
    # print(f"second {u = }, {v = }")
    if v == u + 1:
        return Failure(f"second({u = }, {v = })")
    # print(f"second Success({u = } + {v = })")
    return Success(u + v)


def composed_tuples(i: int, j: int) -> Result[int, str]:
    return flow((i, j), first, bind(second))


inputs = [(1, 1), (2, 3), (4, 3)]
outputs = [composed_tuples(i, j) for i, j in inputs]
for inp, outp in zip(inputs, outputs):
    print(f"{inp}: {outp}")
console == """
(1, 1): <Failure: first(i = 1, j = 1)>
(2, 3): <Failure: second(u = 2, v = 3)>
(4, 3): <Success: 7>
"""
