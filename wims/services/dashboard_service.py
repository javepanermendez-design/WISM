"""Dashboard read model."""
from ..domain.entities import Delivery, Order, Product, StockMovement
from ..repositories.base import BaseRepository


class DashboardService:
    """Build the dashboard's current operational summary."""
    def __init__(self, products: BaseRepository[Product], deliveries: BaseRepository[Delivery], orders, movements, activity: list[dict[str, str]]):
        self.products = products
        self.deliveries = deliveries
        self.orders = orders
        self.movements = movements
        self.activity = activity

    def summary(self) -> dict[str, object]:
        products = self.products.list()
        return {"products": products, "low_products": [p for p in products if p.status.value != "In Stock"], "deliveries": self.deliveries.list(), "orders": self.orders.list(), "activity": self.activity}

    def navigation_counts(self) -> dict[str, int]:
        open_statuses = {"Pending", "Picking", "Ready"}
        return {"low": len([p for p in self.products.list() if p.status.value == "Low Stock"]), "pending": len([o for o in self.orders.list() if o.status.value in open_statuses])}
