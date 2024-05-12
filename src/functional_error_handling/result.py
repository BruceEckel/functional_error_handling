#: result.py
# Add and_then
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

ANSWER = TypeVar("ANSWER")
ERROR = TypeVar("ERROR")


@dataclass(frozen=True)
class Result(Generic[ANSWER, ERROR]):
    def and_then(
        self, func: Callable[[ANSWER], "Result"]
    ) -> "Result[ANSWER, ERROR]":
        if isinstance(self, Success):
            return func(self.unwrap())
        return self  # Pass the Failure forward


@dataclass(frozen=True)
class Success(Result[ANSWER, ERROR]):
    value: ANSWER

    def unwrap(self) -> ANSWER:
        return self.value


@dataclass(frozen=True)
class Failure(Result[ANSWER, ERROR]):
    error: ERROR
