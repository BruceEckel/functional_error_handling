from typing import Generic, TypeVar
from dataclasses import dataclass

T = TypeVar("T")  # Success type
E = TypeVar("E")  # Error type


@dataclass(frozen=True)
class Result(Generic[T, E]):
    pass


@dataclass(frozen=True)
class Ok(Result[T, E]):
    value: T


@dataclass(frozen=True)
class Err(Result[T, E]):
    error: E
