from datetime import date

import pytest

from wims.domain.entities import Delivery, DeliveryItem, Location, Order, OrderItem, Product
from wims.domain.enums import ItemCondition, MovementType, OrderStatus
from wims.domain.exceptions import InsufficientStockError, InvalidTransitionError, ValidationError
from wims.repositories.memory import MovementRepository, ProductRepository
from wims.services.movement_service import MovementService


def product(stock=10):
    return Product(1, "SKU-1", "Test item", "Tools", Location("A", "01", "01"), stock, 5, 20, "each", "Supplier", 1.0)


def test_product_status_and_stock_rules():
    assert product(10).status.value == "In Stock"
    assert product(5).status.value == "Low Stock"
    assert product(0).status.value == "Out of Stock"
    with pytest.raises(InsufficientStockError):
        product(2).release(3)


def test_order_state_machine_and_progress():
    item = OrderItem(1, 2, 0, product(2))
    order = Order(1, "ORD-1", "Customer", OrderStatus.PENDING, date.today(), [item])
    order.transition_to(OrderStatus.PICKING)
    item.pick(2)
    assert order.progress == "2 of 2 picked"
    assert order.can_be_ready
    order.transition_to(OrderStatus.READY)
    order.transition_to(OrderStatus.COMPLETED)
    with pytest.raises(InvalidTransitionError):
        order.transition_to(OrderStatus.PICKING)


def test_delivery_requires_notes_for_damaged_items():
    delivery = Delivery(1, "Supplier", "ASN-1", date.today(), [DeliveryItem(1, 2)], ItemCondition.DAMAGED)
    with pytest.raises(ValidationError):
        delivery.validate()
    delivery.notes = "Two cartons crushed"
    delivery.validate()


def test_movement_service_records_stock_boundaries():
    item = product(10)
    products = ProductRepository([item])
    movements = MovementRepository([])
    service = MovementService(products, movements)
    before, after = item.receive(4)
    movement = service.record(item, MovementType.RECEIVED, 4, before, after, "Maya Chen", "ASN-1")
    assert movement.previous_stock == 10
    assert movement.updated_stock == 14
    assert movement.delta == 4
    assert movement.direction == "up"
