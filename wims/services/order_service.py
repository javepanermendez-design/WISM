"""Order, cancellation, completion, and return use cases."""
from datetime import date

from ..domain.entities import Notification, Order, Product
from ..domain.enums import MovementType, NotificationType, OrderStatus
from ..domain.exceptions import InvalidTransitionError, ValidationError
from ..repositories.base import BaseRepository
from .movement_service import MovementService


class OrderService:
    """Coordinate order state transitions without allowing destructive deletion."""
    def __init__(self, orders: BaseRepository[Order], products: BaseRepository[Product], movements: MovementService, notifications: BaseRepository[Notification] | None = None):
        self.orders = orders
        self.products = products
        self.movements = movements
        self.notifications = notifications

    def list(self, status: str = "Active", query: str = "", date_from: str = "", date_to: str = "") -> list[Order]:
        orders = self.orders.list()
        if status == "Active":
            orders = [order for order in orders if order.status in (OrderStatus.PENDING, OrderStatus.PICKING, OrderStatus.READY)]
        elif status != "All":
            orders = [order for order in orders if order.status.value == status]
        query = query.lower().strip()
        if query:
            orders = [order for order in orders if query in order.number.lower() or query in order.customer.lower()]
        if date_from:
            orders = [order for order in orders if order.created.isoformat() >= date_from]
        if date_to:
            orders = [order for order in orders if order.created.isoformat() <= date_to]
        return orders

    def get(self, order_id: int) -> Order:
        order = self.orders.get(order_id)
        if not order:
            raise ValueError("Order was not found.")
        for line in order.lines:
            line.product = self.products.get(line.product_id)
        order.lines.sort(key=lambda line: (line.product.zone, line.product.location_code))
        return order

    def start_picking(self, order_id: int) -> Order:
        order = self.get(order_id)
        order.transition_to(OrderStatus.PICKING)
        return self.orders.update(order)

    def mark_ready(self, order_id: int) -> Order:
        order = self.get(order_id)
        order.transition_to(OrderStatus.READY)
        return self.orders.update(order)

    def complete(self, order_id: int, user: str) -> Order:
        order = self.get(order_id)
        order.transition_to(OrderStatus.COMPLETED)
        for line in order.lines:
            product = self.products.get(line.product_id)
            previous, updated = product.release(line.quantity)
            self.products.update(product)
            self.movements.record(product, MovementType.RELEASED, line.quantity, previous, updated, user, order.number)
        order.completed_by = user
        order.completed_at = date.today()
        return self.orders.update(order)

    def pick(self, order_id: int, line_index: int) -> Order:
        order = self.get(order_id)
        if order.status != OrderStatus.PICKING:
            raise InvalidTransitionError(f"{order.number} is read-only unless it is in Picking.")
        order.lines[line_index].pick()
        return self.orders.update(order)

    def unpick(self, order_id: int, line_index: int) -> Order:
        order = self.get(order_id)
        if order.status != OrderStatus.PICKING:
            raise InvalidTransitionError(f"{order.number} is read-only unless it is in Picking.")
        order.lines[line_index].unpick()
        return self.orders.update(order)

    def cancel(self, order_id: int, reason: str) -> Order:
        order = self.get(order_id)
        order.cancel(reason)
        saved = self.orders.update(order)
        if self.notifications:
            notification_id = max((item.id for item in self.notifications.list()), default=0) + 1
            self.notifications.add(Notification(notification_id, "Order cancelled", f"{order.number} was cancelled: {order.cancel_reason}", True, "Today", NotificationType.ORDER))
        return saved

    def create_return(self, order_id: int, user: str) -> Order:
        order = self.get(order_id)
        if order.status != OrderStatus.COMPLETED:
            raise InvalidTransitionError("Returns can only be created for completed orders.")
        for line in order.lines:
            product = self.products.get(line.product_id)
            previous, updated = product.receive(line.quantity)
            self.products.update(product)
            self.movements.record(product, MovementType.RECEIVED, line.quantity, previous, updated, user, f"RETURN-{order.number}")
        return order
