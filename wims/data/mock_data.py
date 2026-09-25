"""Adapter that turns the existing mock dictionaries into domain entities."""
from datetime import date, timedelta

import mock_data as legacy

from ..domain.entities import (Category, Delivery, DeliveryItem, Location,
							   Notification, Order, OrderItem, Product,
							   StockMovement, Supplier, User)
from ..domain.enums import ItemCondition, MovementType, OrderStatus, Role


def users() -> list[User]:
	"""Build users from the prototype records."""
	return [
		User(
			item["id"],
			item["name"],
			Role(item["role"]),
			item["initials"],
			f"{item['name'].split()[0].lower()}@wims.test",
			date.today() - timedelta(days=365 + index * 42),
		)
		for index, item in enumerate(legacy.USERS)
	]


def suppliers() -> list[Supplier]:
	return [Supplier(index, name) for index, name in enumerate(legacy.SUPPLIERS, 1)]


def categories() -> list[Category]:
	return [Category(index, name) for index, name in enumerate(legacy.CATEGORIES, 1)]


def products() -> list[Product]:
	return [Product(item["id"], item["sku"], item["name"], item["category"], Location(item["zone"], item["aisle"], item["bin"]), item["stock"], item["min_stock"], item["max_stock"], item["unit"], item["supplier"], item["price"], date.fromisoformat(item["expiry_date"]) if item.get("expiry_date") else None) for item in legacy.products]


def deliveries() -> list[Delivery]:
	return [Delivery(item["id"], item["supplier"], item["delivery_no"], date.fromisoformat(item["date"]), [DeliveryItem(line["product_id"], line["quantity"]) for line in item["lines"]]) for item in legacy.expected_deliveries]


def orders() -> list[Order]:
	return [Order(item["id"], item["number"], item["customer"], OrderStatus(item["status"]), date.fromisoformat(item["created"]), [OrderItem(line["product_id"], line["quantity"], line["picked"]) for line in item["lines"]], item.get("completed_by"), date.fromisoformat(item["completed_at"]) if item.get("completed_at") else None) for item in legacy.orders]


def movements() -> list[StockMovement]:
	return [StockMovement(item["id"], item["product_id"], MovementType(item["type"]), item["quantity"], item["previous"], item["updated"], item["user"], item["reference"], date.fromisoformat(item["created"])) for item in legacy.movements]


def notifications() -> list[Notification]:
	return [Notification(item["id"], item["title"], item["body"], item["unread"], item["created"]) for item in legacy.notifications]


def activity() -> list[dict[str, str]]:
	return legacy.activity.copy()
