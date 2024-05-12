#: result_basic.py
# Result with Success & Failure subtypes
from dataclasses import dataclass
from typing import Generic, TypeVar

ANSWER = TypeVar("ANSWER")  # Generic parameters
ERROR = TypeVar("ERROR")


@dataclass(frozen=True)
class Result(Generic[ANSWER, ERROR]):
    pass


@dataclass(frozen=True)
class Success(Result[ANSWER, ERROR]):
    value: ANSWER  # Usage: return Success(answer)

    def unwrap(self) -> ANSWER:
        return self.value


@dataclass(frozen=True)
class Failure(Result[ANSWER, ERROR]):
    error: ERROR  # Usage: return Success(error)
