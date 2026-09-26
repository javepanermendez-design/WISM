"""Dependency-injection container for the application."""
from dataclasses import dataclass

from .data import mock_data
from .persistence import build_snapshot, restore_entities, save_session_state, should_persist
from .repositories.memory import (CategoryRepository, DeliveryRepository,
                                  InMemoryRepository, LocationRepository,
                                  MovementRepository, NotificationRepository,
                                  OrderRepository, ProductRepository,
                                  SupplierRepository, UserRepository)
from .services.auth_service import AuthService
from .services.dashboard_service import DashboardService
from .services.inventory_service import InventoryService
from .services.movement_service import MovementService
from .services.notification_service import NotificationService
from .services.order_service import OrderService
from .services.receiving_service import ReceivingService


@dataclass
class Container:
    """Own repositories and wire services through constructors."""
    auth: AuthService
    inventory: InventoryService
    receiving: ReceivingService
    orders: OrderService
    movements: MovementService
    notifications: NotificationService
    dashboard: DashboardService
    categories: list[str]
    zones: list[str]
    zone_names: dict[str, str]
    suppliers: list[str]

    @classmethod
    def build(cls) -> "Container":
        user_repo = UserRepository(restore_entities("users", mock_data.users()))
        products = restore_entities("products", mock_data.products())
        product_repo = ProductRepository(products)
        movement_repo = MovementRepository(restore_entities("movements", mock_data.movements()))
        order_repo = OrderRepository(restore_entities("orders", mock_data.orders()))
        delivery_repo = DeliveryRepository(restore_entities("deliveries", mock_data.deliveries()))
        notification_repo = NotificationRepository(restore_entities("notifications", mock_data.notifications()))

        def persist_state() -> None:
            if not should_persist():
                return
            save_session_state(build_snapshot({
                "users": user_repo.list(),
                "suppliers": SupplierRepository(restore_entities("suppliers", mock_data.suppliers())).list(),
                "categories": CategoryRepository(restore_entities("categories", mock_data.categories())).list(),
                "products": product_repo.list(),
                "deliveries": delivery_repo.list(),
                "orders": order_repo.list(),
                "movements": movement_repo.list(),
                "notifications": notification_repo.list(),
            }))

        for repo in (user_repo, product_repo, movement_repo, order_repo, delivery_repo, notification_repo):
            repo.set_persistence_callback(persist_state)

        movement_service = MovementService(product_repo, movement_repo)
        order_service = OrderService(order_repo, product_repo, movement_service, notification_repo)
        inventory_service = InventoryService(product_repo, movement_repo, order_repo, delivery_repo)
        return cls(
            AuthService(user_repo), inventory_service,
            ReceivingService(delivery_repo, product_repo, movement_service),
            order_service, movement_service,
            NotificationService(notification_repo),
            DashboardService(product_repo, delivery_repo, order_service, movement_service, mock_data.activity()),
            [item.name for item in mock_data.categories()], mock_data.legacy.ZONES, mock_data.legacy.ZONE_NAMES,
            [item.name for item in mock_data.suppliers()],
        )
