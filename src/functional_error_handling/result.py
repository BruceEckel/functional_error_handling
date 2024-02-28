from typing import TypeVar, Generic
from dataclasses import dataclass

T = TypeVar("T")  # Success type
E = TypeVar("E")  # Error type


@dataclass(frozen=True)
class Result(Generic[T, E]):
    value: T | E
    error: bool

    @classmethod
    def Ok(cls, value: T) -> "Result[T, E]":
        return cls(value, False)

    @classmethod
    def Err(cls, error: E) -> "Result[T, E]":
        return cls(error, True)

    def __repr__(self) -> str:
        if self.error:
            return f"Error({self.value})"
        else:
            return f"Ok({self.value})"
