"""Polymorphic report contract."""
from abc import ABC, abstractmethod


class Report(ABC):
    """Shared report interface with optional filters."""
    def __init__(self, items: list[object]):
        self.items = items

    @abstractmethod
    def build(self) -> list[object]: ...

    @abstractmethod
    def to_rows(self) -> list[dict[str, object]]: ...
