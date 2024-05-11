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
        if isinstance(self, Ok):
            return func(self.value)
        return self  # Pass the Err forward


@dataclass(frozen=True)
class Ok(Result[ANSWER, ERROR]):
    value: ANSWER

    def unwrap(self) -> ANSWER:
        return self.value


@dataclass(frozen=True)
class Err(Result[ANSWER, ERROR]):
    error: ERROR
