"""Stock movement recording use cases."""
from datetime import date
from ..domain.entities import Product, StockMovement
from ..domain.enums import MovementType
from ..repositories.base import BaseRepository


class MovementService:
    """Record immutable movements for every stock change."""
    def __init__(self, products: BaseRepository[Product], movements: BaseRepository[StockMovement]):
        self.products = products
        self.movements = movements

    def record(self, product: Product, movement_type: MovementType, quantity: int, previous: int, updated: int, user: str, reference: str) -> StockMovement:
        movement = StockMovement(len(self.movements.list()) + 1, product.id, movement_type, quantity, previous, updated, user, reference, date.today())
        self.movements.add(movement)
        return movement

    def history(self, product_id: int | None = None, reference: str | None = None) -> list[StockMovement]:
        records = self.movements.list()
        if product_id:
            records = [item for item in records if item.product_id == product_id]
        if reference:
            records = [item for item in records if item.reference == reference]
        return records

    def adjust(self, product_id: int, quantity: int, reason: str, user: str) -> StockMovement:
        product = self.products.get(product_id)
        previous, updated = product.adjust(quantity, reason)
        self.products.update(product)
        return self.record(product, MovementType.ADJUSTED, abs(quantity), previous, updated, user, "ADJUSTMENT")
