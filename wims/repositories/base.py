"""Repository contracts."""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    """Minimal persistence contract used by services."""
    @abstractmethod
    def get(self, entity_id: int) -> T | None: ...

    @abstractmethod
    def list(self) -> list[T]: ...

    @abstractmethod
    def add(self, entity: T) -> T: ...

    @abstractmethod
    def update(self, entity: T) -> T: ...

    @abstractmethod
    def delete(self, entity_id: int) -> None: ...
