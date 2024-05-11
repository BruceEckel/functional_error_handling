#: result_basic.py
# Result with OK & Err subtypes
from dataclasses import dataclass
from typing import Generic, TypeVar

ANSWER = TypeVar("ANSWER")  # Generic parameters
ERROR = TypeVar("ERROR")


@dataclass(frozen=True)
class Result(Generic[ANSWER, ERROR]):
    pass


@dataclass(frozen=True)
class Ok(Result[ANSWER, ERROR]):
    value: ANSWER  # Usage: return Ok(answer)

    def unwrap(self) -> ANSWER:
        return self.value


@dataclass(frozen=True)
class Err(Result[ANSWER, ERROR]):
    error: ERROR  # Usage: return Err(error)
