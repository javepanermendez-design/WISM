"""Lightweight JSON persistence for the prototype's in-memory repositories."""
from __future__ import annotations

import json
import os
from dataclasses import fields, is_dataclass
from datetime import date
from enum import Enum
from pathlib import Path
from typing import Any

from .domain.entities import (
    Category,
    Delivery,
    DeliveryItem,
    Location,
    Notification,
    Order,
    OrderItem,
    Product,
    StockMovement,
    Supplier,
    User,
)
from .domain.enums import ItemCondition, MovementType, NotificationType, OrderStatus, Role


def session_state_path() -> Path:
    """Return the default on-disk location for the persisted session snapshot."""
    default_path = Path(__file__).resolve().parent.parent / "data" / "session_state.json"
    return Path(os.getenv("WIMS_SESSION_PATH", str(default_path)))


def should_persist() -> bool:
    """Only persist when the app is not running under pytest unless the path is explicitly overridden."""
    if os.getenv("WIMS_DISABLE_PERSISTENCE", "").lower() in {"1", "true", "yes"}:
        return False
    if os.getenv("WIMS_SESSION_PATH"):
        return True
    return not bool(os.environ.get("PYTEST_CURRENT_TEST"))


def load_session_state(path: str | Path | None = None) -> dict[str, list[dict[str, Any]]]:
    """Load a serialized repository snapshot if one exists."""
    target = Path(path) if path is not None else session_state_path()
    if not target.exists():
        return {}
    try:
        payload = json.loads(target.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    if isinstance(payload, dict):
        return payload
    return {}


def save_session_state(snapshot: dict[str, list[Any]], path: str | Path | None = None) -> None:
    """Persist the current in-memory repository state to JSON."""
    target = Path(path) if path is not None else session_state_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(snapshot, indent=2, default=_json_default), encoding="utf-8")


def restore_entities(key: str, fallback: list[Any]) -> list[Any]:
    """Return the persisted items for a repository if available, otherwise use the mock seed data."""
    payload = load_session_state()
    raw_items = payload.get(key)
    if not raw_items:
        return fallback
    return [_restore_entity(key, item) for item in raw_items]


def build_snapshot(entities_by_key: dict[str, list[Any]]) -> dict[str, list[dict[str, Any]]]:
    """Convert a repository state map into JSON-safe structures."""
    return {key: [_json_value(item) for item in items] for key, items in entities_by_key.items()}


def _json_default(value: Any) -> Any:
    if is_dataclass(value):
        return {field.name: _json_value(getattr(value, field.name)) for field in fields(value)}
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, Path):
        return str(value)
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")


def _json_value(value: Any) -> Any:
    if is_dataclass(value):
        return {field.name: _json_value(getattr(value, field.name)) for field in fields(value)}
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(key): _json_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_value(item) for item in value]
    return value


def _restore_entity(key: str, payload: dict[str, Any]) -> Any:
    builders = {
        "users": _restore_user,
        "suppliers": _restore_supplier,
        "categories": _restore_category,
        "products": _restore_product,
        "deliveries": _restore_delivery,
        "orders": _restore_order,
        "movements": _restore_stock_movement,
        "notifications": _restore_notification,
    }
    builder = builders.get(key)
    if builder is None:
        return payload
    return builder(payload)


def _restore_user(payload: dict[str, Any]) -> User:
    return User(
        id=payload["id"],
        name=payload["name"],
        role=Role(payload["role"]),
        initials=payload["initials"],
        email=payload.get("email", ""),
        created_at=date.fromisoformat(payload["created_at"]) if payload.get("created_at") else None,
    )


def _restore_supplier(payload: dict[str, Any]) -> Supplier:
    return Supplier(id=payload["id"], name=payload["name"])


def _restore_category(payload: dict[str, Any]) -> Category:
    return Category(id=payload["id"], name=payload["name"])


def _restore_location(payload: dict[str, Any]) -> Location:
    return Location(zone=payload["zone"], aisle=payload["aisle"], bin=payload["bin"])


def _restore_stock_movement(payload: dict[str, Any]) -> StockMovement:
    return StockMovement(
        id=payload["id"],
        product_id=payload["product_id"],
        movement_type=MovementType(payload["movement_type"]),
        quantity=payload["quantity"],
        previous_stock=payload["previous_stock"],
        updated_stock=payload["updated_stock"],
        user=payload["user"],
        reference=payload["reference"],
        created=date.fromisoformat(payload["created"]),
    )


def _restore_notification(payload: dict[str, Any]) -> Notification:
    return Notification(
        id=payload["id"],
        title=payload["title"],
        body=payload["body"],
        unread=payload["unread"],
        created=payload["created"],
        kind=NotificationType(payload["kind"]) if payload.get("kind") else NotificationType.SYSTEM,
    )


def _restore_product(payload: dict[str, Any]) -> Product:
    location = payload.get("location")
    raw_movements = payload.get("movements") or []
    return Product(
        id=payload["id"],
        sku=payload["sku"],
        name=payload["name"],
        category=payload["category"],
        location=_restore_location(location) if isinstance(location, dict) else Location("A", "00", "00"),
        stock=payload["stock"],
        min_stock=payload["min_stock"],
        max_stock=payload["max_stock"],
        unit=payload["unit"],
        supplier=payload["supplier"],
        price=payload["price"],
        expiry_date=date.fromisoformat(payload["expiry_date"]) if payload.get("expiry_date") else None,
        archived=payload.get("archived", False),
        movements=[_restore_stock_movement(item) for item in raw_movements],
    )


def _restore_delivery_item(payload: dict[str, Any]) -> DeliveryItem:
    return DeliveryItem(product_id=payload["product_id"], quantity=payload["quantity"])


def _restore_delivery(payload: dict[str, Any]) -> Delivery:
    return Delivery(
        id=payload["id"],
        supplier=payload["supplier"],
        delivery_no=payload["delivery_no"],
        arrival_date=date.fromisoformat(payload["arrival_date"]),
        items=[_restore_delivery_item(item) for item in payload.get("items", [])],
        condition=ItemCondition(payload["condition"]) if payload.get("condition") else ItemCondition.GOOD,
        notes=payload.get("notes", ""),
        status=payload.get("status", "Expected"),
    )


def _restore_order_item(payload: dict[str, Any]) -> OrderItem:
    return OrderItem(
        product_id=payload["product_id"],
        quantity=payload["quantity"],
        picked=payload.get("picked", 0),
        product=None,
    )


def _restore_order(payload: dict[str, Any]) -> Order:
    return Order(
        id=payload["id"],
        number=payload["number"],
        customer=payload["customer"],
        status=OrderStatus(payload["status"]),
        created=date.fromisoformat(payload["created"]),
        lines=[_restore_order_item(item) for item in payload.get("lines", [])],
        completed_by=payload.get("completed_by"),
        completed_at=date.fromisoformat(payload["completed_at"]) if payload.get("completed_at") else None,
        cancel_reason=payload.get("cancel_reason"),
    )
