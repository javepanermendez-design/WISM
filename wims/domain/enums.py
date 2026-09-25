"""Domain enumerations used by WIMS."""
from enum import StrEnum


class StockStatus(StrEnum):
    IN_STOCK = "In Stock"
    LOW_STOCK = "Low Stock"
    OUT_OF_STOCK = "Out of Stock"


class OrderStatus(StrEnum):
    PENDING = "Pending"
    PICKING = "Picking"
    READY = "Ready"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class MovementType(StrEnum):
    RECEIVED = "Received"
    RELEASED = "Released"
    TRANSFERRED = "Transferred"
    ADJUSTED = "Adjusted"


class ItemCondition(StrEnum):
    GOOD = "Good"
    DAMAGED = "Damaged"
    INCOMPLETE = "Incomplete"


class Role(StrEnum):
    SUPERVISOR = "Inventory supervisor"
    RECEIVING_CLERK = "Receiving clerk"
    PICKER = "Picker"


class NotificationType(StrEnum):
    STOCK = "Stock"
    DELIVERY = "Delivery"
    ORDER = "Order"
    SYSTEM = "System"
