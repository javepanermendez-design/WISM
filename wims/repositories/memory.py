"""In-memory repository implementations."""
from typing import Generic, TypeVar
from .base import BaseRepository

T = TypeVar("T")


class InMemoryRepository(BaseRepository[T], Generic[T]):
    """Dictionary-backed repository for the prototype."""
    def __init__(self, entities: list[T] | None = None):
        self._items = {getattr(item, "id"): item for item in entities or []}

    def get(self, entity_id: int) -> T | None:
        return self._items.get(int(entity_id))

    def list(self) -> list[T]:
        return list(self._items.values())

    def add(self, entity: T) -> T:
        self._items[getattr(entity, "id")] = entity
        return entity

    def update(self, entity: T) -> T:
        self._items[getattr(entity, "id")] = entity
        return entity

    def delete(self, entity_id: int) -> None:
        self._items.pop(int(entity_id), None)


class UserRepository(InMemoryRepository[T]): pass
class SupplierRepository(InMemoryRepository[T]): pass
class CategoryRepository(InMemoryRepository[T]): pass
class LocationRepository(InMemoryRepository[T]): pass
class ProductRepository(InMemoryRepository[T]): pass
class DeliveryRepository(InMemoryRepository[T]): pass
class OrderRepository(InMemoryRepository[T]): pass
class MovementRepository(InMemoryRepository[T]): pass
class NotificationRepository(InMemoryRepository[T]): pass
