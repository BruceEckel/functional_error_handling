#: result.py
# Result with OK & Err subtypes
from typing import Generic, TypeVar
from dataclasses import dataclass

ANSWER = TypeVar("ANSWER")
ERROR = TypeVar("ERROR")


@dataclass(frozen=True)
class Result(Generic[ANSWER, ERROR]):
    pass


@dataclass(frozen=True)
class Ok(Result[ANSWER, ERROR]):
    value: ANSWER  # Return Ok(answer)


@dataclass(frozen=True)
class Err(Result[ANSWER, ERROR]):
    error: ERROR  # Return Err(error)
