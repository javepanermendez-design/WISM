"""In-memory repository implementations."""
from typing import Callable, Generic, TypeVar

from .base import BaseRepository

T = TypeVar("T")


class InMemoryRepository(BaseRepository[T], Generic[T]):
    """Dictionary-backed repository for the prototype."""
    def __init__(self, entities: list[T] | None = None, persist_callback: Callable[[], None] | None = None):
        self._items = {getattr(item, "id"): item for item in entities or []}
        self._persist_callback = persist_callback

    def set_persistence_callback(self, callback: Callable[[], None] | None) -> None:
        self._persist_callback = callback

    def _persist(self) -> None:
        if self._persist_callback is not None:
            self._persist_callback()

    def get(self, entity_id: int) -> T | None:
        return self._items.get(int(entity_id))

    def list(self) -> list[T]:
        return list(self._items.values())

    def add(self, entity: T) -> T:
        self._items[getattr(entity, "id")] = entity
        self._persist()
        return entity

    def update(self, entity: T) -> T:
        self._items[getattr(entity, "id")] = entity
        self._persist()
        return entity

    def delete(self, entity_id: int) -> None:
        self._items.pop(int(entity_id), None)
        self._persist()


class UserRepository(InMemoryRepository[T]): pass
class SupplierRepository(InMemoryRepository[T]): pass
class CategoryRepository(InMemoryRepository[T]): pass
class LocationRepository(InMemoryRepository[T]): pass
class ProductRepository(InMemoryRepository[T]): pass
class DeliveryRepository(InMemoryRepository[T]): pass
class OrderRepository(InMemoryRepository[T]): pass
class MovementRepository(InMemoryRepository[T]): pass
class NotificationRepository(InMemoryRepository[T]): pass
