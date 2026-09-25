"""Concrete warehouse reports."""
from .base import Report


class InventoryReport(Report):
    def build(self): return self.items
    def to_rows(self): return [{"sku": item.sku, "name": item.name, "stock": item.stock, "status": item.status.value} for item in self.items]


class LowStockReport(InventoryReport):
    def build(self): return [item for item in self.items if item.status.value != "In Stock"]


class MovementReport(Report):
    def build(self): return self.items
    def to_rows(self): return [{"reference": item.reference, "type": item.type, "delta": item.delta, "date": item.created.isoformat()} for item in self.items]


class OrderReport(Report):
    def build(self): return self.items
    def to_rows(self): return [{"number": item.number, "customer": item.customer, "status": item.status.value, "progress": item.progress} for item in self.items]
