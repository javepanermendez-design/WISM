"""Business entities and their invariants."""
from dataclasses import dataclass, field
from datetime import date
from typing import Optional

from .enums import ItemCondition, MovementType, NotificationType, OrderStatus, Role, StockStatus
from .exceptions import InsufficientStockError, InvalidTransitionError, ValidationError


@dataclass
class User:
    id: int
    name: str
    role: Role
    initials: str
    email: str = ""
    created_at: date | None = None


@dataclass
class Supplier:
    id: int
    name: str


@dataclass
class Category:
    id: int
    name: str


@dataclass
class Location:
    zone: str
    aisle: str
    bin: str

    @property
    def code(self) -> str:
        return f"{self.zone}-{self.aisle}-{self.bin}"


@dataclass
class Product:
    id: int
    sku: str
    name: str
    category: str
    location: Location
    stock: int
    min_stock: int
    max_stock: int
    unit: str
    supplier: str
    price: float
    expiry_date: date | None = None
    archived: bool = False
    movements: list["StockMovement"] = field(default_factory=list)

    @property
    def zone(self) -> str:
        return self.location.zone

    @property
    def aisle(self) -> str:
        return self.location.aisle

    @property
    def bin(self) -> str:
        return self.location.bin

    @property
    def location_code(self) -> str:
        return self.location.code

    @property
    def expiry_days(self) -> int | None:
        return (self.expiry_date - date.today()).days if self.expiry_date else None

    @property
    def status(self) -> StockStatus:
        if self.stock == 0:
            return StockStatus.OUT_OF_STOCK
        if self.stock <= self.min_stock:
            return StockStatus.LOW_STOCK
        return StockStatus.IN_STOCK

    def receive(self, quantity: int) -> tuple[int, int]:
        self._validate_quantity(quantity)
        before = self.stock
        self.stock += quantity
        return before, self.stock

    def release(self, quantity: int) -> tuple[int, int]:
        self._validate_quantity(quantity)
        if quantity > self.stock:
            raise InsufficientStockError(f"Only {self.stock} {self.unit} available for {self.name}.")
        before = self.stock
        self.stock -= quantity
        return before, self.stock

    def adjust(self, quantity: int, reason: str) -> tuple[int, int]:
        if not reason.strip():
            raise ValidationError("Add a reason before adjusting stock.")
        before = self.stock
        if self.stock + quantity < 0:
            raise InsufficientStockError(f"Adjustment would take {self.name} below zero stock.")
        self.stock += quantity
        return before, self.stock

    def archive(self) -> None:
        self.archived = True

    def restore(self) -> None:
        self.archived = False

    @staticmethod
    def _validate_quantity(quantity: int) -> None:
        if quantity <= 0:
            raise ValidationError("Quantity must be greater than zero.")


@dataclass
class DeliveryItem:
    product_id: int
    quantity: int


@dataclass
class Delivery:
    id: int
    supplier: str
    delivery_no: str
    arrival_date: date
    items: list[DeliveryItem]
    condition: ItemCondition = ItemCondition.GOOD
    notes: str = ""
    status: str = "Expected"

    @property
    def date(self) -> str:
        return self.arrival_date.isoformat()

    def validate(self) -> None:
        if any(item.quantity <= 0 for item in self.items):
            raise ValidationError("Every delivery line must have a positive quantity.")
        if self.condition in (ItemCondition.DAMAGED, ItemCondition.INCOMPLETE) and not self.notes.strip():
            raise ValidationError("Add notes when a delivery is damaged or incomplete.")

    def stock_preview(self, products: dict[int, Product]) -> list[tuple[Product, int, int]]:
        self.validate()
        preview = []
        for item in self.items:
            product = products[item.product_id]
            preview.append((product, product.stock, product.stock + item.quantity))
        return preview


@dataclass
class OrderItem:
    product_id: int
    quantity: int
    picked: int = 0
    product: Optional[Product] = None

    @property
    def available_qty(self) -> int:
        return self.product.stock if self.product else 0

    @property
    def is_short(self) -> bool:
        return self.available_qty < self.quantity - self.picked

    def pick(self, quantity: int = 1) -> None:
        if self.picked + quantity > self.available_qty:
            raise InsufficientStockError(f"Only {self.available_qty} available to pick.")
        self.picked += quantity

    def unpick(self, quantity: int = 1) -> None:
        self.picked = max(0, self.picked - quantity)


@dataclass
class Order:
    id: int
    number: str
    customer: str
    status: OrderStatus
    created: date
    lines: list[OrderItem]
    completed_by: str | None = None
    completed_at: date | None = None
    cancel_reason: str | None = None

    @property
    def progress(self) -> str:
        return f"{sum(line.picked for line in self.lines)} of {sum(line.quantity for line in self.lines)} picked"

    @property
    def can_be_ready(self) -> bool:
        return all(line.picked >= line.quantity for line in self.lines) and not self.has_shortage

    @property
    def has_shortage(self) -> bool:
        return any(line.is_short for line in self.lines)

    def transition_to(self, target: OrderStatus) -> None:
        allowed = {OrderStatus.PENDING: OrderStatus.PICKING, OrderStatus.PICKING: OrderStatus.READY, OrderStatus.READY: OrderStatus.COMPLETED}
        if allowed.get(self.status) != target:
            raise InvalidTransitionError(f"{self.number} cannot move from {self.status} to {target}.")
        if target == OrderStatus.READY and not self.can_be_ready:
            raise InvalidTransitionError(f"{self.number} needs every item picked before it can be ready.")
        self.status = target

    def cancel(self, reason: str) -> None:
        if not reason.strip():
            raise ValidationError("A cancellation reason is required.")
        if self.status in (OrderStatus.COMPLETED, OrderStatus.CANCELLED):
            raise InvalidTransitionError(f"{self.number} cannot be cancelled from {self.status}.")
        self.status = OrderStatus.CANCELLED
        self.cancel_reason = reason.strip()


@dataclass(frozen=True)
class StockMovement:
    id: int
    product_id: int
    movement_type: MovementType
    quantity: int
    previous_stock: int
    updated_stock: int
    user: str
    reference: str
    created: date

    @property
    def delta(self) -> int:
        return self.updated_stock - self.previous_stock

    @property
    def direction(self) -> str:
        return "up" if self.delta > 0 else "down" if self.delta < 0 else "neutral"

    @property
    def type(self) -> str:
        return self.movement_type.value


@dataclass
class Notification:
    id: int
    title: str
    body: str
    unread: bool
    created: str
    kind: NotificationType = NotificationType.SYSTEM
