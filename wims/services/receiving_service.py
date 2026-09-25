"""Receiving use cases."""
from ..domain.entities import Delivery, Product
from ..domain.enums import MovementType
from ..repositories.base import BaseRepository
from .movement_service import MovementService


class ReceivingService:
    """Validate deliveries and apply stock receipts."""
    def __init__(self, deliveries: BaseRepository[Delivery], products: BaseRepository[Product], movements: MovementService):
        self.deliveries = deliveries
        self.products = products
        self.movements = movements

    def get_expected(self, delivery_id: int | None = None) -> Delivery:
        return self.deliveries.get(delivery_id) if delivery_id else self.deliveries.list()[0]

    def preview(self, delivery: Delivery) -> list[tuple[Product, int, int]]:
        return delivery.stock_preview({p.id: p for p in self.products.list()})

    def confirm(self, delivery: Delivery, user: str) -> list[tuple[Product, int, int]]:
        if delivery.status != "Expected":
            raise ValidationError("This delivery has already been received.")
        preview = self.preview(delivery)
        for item, before, after in preview:
            item.receive(after - before)
            self.products.update(item)
            self.movements.record(item, MovementType.RECEIVED, after - before, before, after, user, delivery.delivery_no)
        delivery.status = "Received"
        self.deliveries.update(delivery)
        return preview
