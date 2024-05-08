#: result.py
# Result with OK & Err subtypes
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

ANSWER = TypeVar("ANSWER")
ERROR = TypeVar("ERROR")


@dataclass(frozen=True)
class Result(Generic[ANSWER, ERROR]):
    # Ignore this method for now:
    def and_then(self, func: Callable[[ANSWER], "Result"]) -> "Result[ANSWER, ERROR]":
        if isinstance(self, Ok):
            return func(self.value)
        return self  # Just pass the Err forward


@dataclass(frozen=True)
class Ok(Result[ANSWER, ERROR]):
    value: ANSWER  # Usage: return Ok(answer)

    def unwrap(self) -> ANSWER:
        return self.value


@dataclass(frozen=True)
class Err(Result[ANSWER, ERROR]):
    error: ERROR  # Usage: return Err(error)
