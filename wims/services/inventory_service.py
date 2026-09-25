"""Inventory use cases."""
import re
from datetime import date

from ..domain.entities import Delivery, Order, Product
from ..domain.exceptions import DuplicateSkuError, ValidationError, WimsError
from ..repositories.base import BaseRepository
from .movement_service import MovementService


class InventoryService:
    """Search, maintain, and archive products."""
    def __init__(self, products: BaseRepository[Product], movements: BaseRepository, orders: BaseRepository[Order] | None = None, deliveries: BaseRepository[Delivery] | None = None):
        self.products = products
        self.movements = movements
        self.orders = orders
        self.deliveries = deliveries

    def list(self, query: str = "", status: str = "", zone: str = "") -> list[Product]:
        query = query.lower()
        result = [p for p in self.products.list() if not p.archived and (not query or query in p.name.lower() or query in p.sku.lower()) and (not status or p.status.value.lower().startswith(status.lower())) and (not zone or p.zone == zone)]
        for product in result:
            product.movements = [movement for movement in self.movements.list() if movement.product_id == product.id][-5:]
        return result

    def get(self, product_id: int) -> Product | None:
        product = self.products.get(product_id)
        if product:
            product.movements = [movement for movement in self.movements.list() if movement.product_id == product.id][-5:]
        return product

    def save(self, product: Product) -> Product:
        self.validate(product)
        duplicate = next((p for p in self.products.list() if p.sku == product.sku and p.id != product.id), None)
        if duplicate:
            raise DuplicateSkuError(f"SKU {product.sku} is already assigned to {duplicate.name}.")
        return self.products.update(product)

    def create(self, product: Product) -> Product:
        self.validate(product)
        if any(item.sku == product.sku for item in self.products.list()):
            raise DuplicateSkuError(f"SKU {product.sku} is already assigned to another product.")
        product.id = max((item.id for item in self.products.list()), default=0) + 1
        return self.products.add(product)

    def validate(self, product: Product) -> None:
        if not product.name.strip():
            raise ValidationError("Product name is required.")
        if not re.fullmatch(r"[A-Z]{2}-\d{4}", product.sku):
            raise ValidationError("SKU must use the format RG-0001.")
        if product.stock < 0 or product.min_stock < 0 or product.max_stock < 1:
            raise ValidationError("Quantities must be zero or greater, and maximum stock must be positive.")
        if product.expiry_date and product.expiry_date < date.today():
            raise ValidationError("Expiry date cannot be in the past.")
        if product.category in {"Dairy & Frozen", "Canned Goods", "Snacks & Biscuits", "Noodles & Pasta"} and not product.expiry_date:
            raise ValidationError(f"Expiry date is required for {product.category}.")

    def archive(self, product_id: int) -> None:
        product = self.products.get(product_id)
        if not product:
            raise WimsError("Product was not found.")
        if self.orders and any(order.status.value in ("Pending", "Picking") and any(line.product_id == product_id for line in order.lines) for order in self.orders.list()):
            raise WimsError(f"Cannot delete {product.name}: it is used by a pending or picking order. View orders to resolve it.")
        if self.deliveries and any(delivery.status == "Expected" and any(line.product_id == product_id for line in delivery.items) for delivery in self.deliveries.list()):
            raise WimsError(f"Cannot delete {product.name}: it is included in an expected delivery. View receiving to resolve it.")
        product.archive()
        self.products.update(product)

    def restore(self, product_id: int) -> None:
        product = self.products.get(product_id)
        if not product:
            raise WimsError("Product was not found.")
        product.restore()
        self.products.update(product)
