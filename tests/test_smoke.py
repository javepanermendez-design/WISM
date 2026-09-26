import pytest

from wims import create_app
from wims.domain.exceptions import InvalidTransitionError, ValidationError


@pytest.fixture
def client():
    app = create_app()
    client = app.test_client()
    client.post("/login", data={"email": "admin@gmail.com", "password": "warehouse"})
    return app, client


def test_routes_render_for_authenticated_user(client):
    _, browser = client
    paths = ["/", "/inventory", "/inventory?status=low", "/inventory/1", "/inventory/new", "/inventory/1/edit", "/receiving", "/orders", "/orders/1", "/movements", "/reports"]
    assert all(browser.get(path).status_code == 200 for path in paths)
    assert browser.get("/inventory/999").status_code == 404


def test_add_product_and_duplicate_sku(client):
    app, browser = client
    form = {"name": "Test Grocery Case", "sku": "CG-9999", "category": "Canned Goods", "unit": "case", "supplier": "Amianan Grain Mill", "expiry_date": "2030-01-01", "stock": "4", "min_stock": "2", "max_stock": "20", "zone": "A", "aisle": "09", "bin": "09", "price": "55"}
    response = browser.post("/inventory/new", data=form)
    assert response.status_code == 302
    assert "created=" in response.location
    assert any(product.sku == "CG-9999" for product in app.container.inventory.products.list())
    assert browser.post("/inventory/new", data=form).status_code == 422


def test_delete_and_undo_product(client):
    app, browser = client
    product = app.container.inventory.get(45)
    assert browser.post(f"/inventory/{product.id}/delete").status_code == 302
    assert product.archived
    assert browser.post(f"/inventory/{product.id}/restore").status_code == 302
    assert not product.archived


def test_receiving_confirm_updates_stock_and_movement(client):
    app, browser = client
    delivery = app.container.receiving.get_expected()
    product = app.container.inventory.get(delivery.items[0].product_id)
    before = product.stock
    assert browser.post("/receiving", data={"action": "review"}).status_code == 302
    assert browser.post("/receiving?step=review", data={"action": "confirm"}).status_code == 302
    assert product.stock == before + delivery.items[0].quantity
    movement = app.container.movements.history(product.id)[-1]
    assert movement.previous_stock == before
    assert movement.updated_stock == product.stock


def test_order_completion_releases_stock_and_records_movement(client):
    app, browser = client
    order = app.container.orders.get(3)
    product = app.container.inventory.get(order.lines[0].product_id)
    before = product.stock
    assert browser.post("/orders/3", data={"action": "complete"}).status_code == 302
    assert order.status.value == "Completed"
    assert product.stock == before - order.lines[0].quantity
    assert app.container.movements.history(product.id)[-1].type == "Released"


def test_completed_order_is_read_only(client):
    app, _ = client
    order = app.container.orders.get(4)
    with pytest.raises(InvalidTransitionError):
        app.container.orders.pick(order.id, 0)
    with pytest.raises(InvalidTransitionError):
        app.container.orders.unpick(order.id, 0)


def test_cancel_requires_reason_and_creates_notification(client):
    app, browser = client
    order = app.container.orders.get(1)
    with pytest.raises(ValidationError):
        app.container.orders.cancel(order.id, "")
    before = app.container.dashboard.navigation_counts()["pending"]
    assert browser.post(f"/orders/{order.id}/cancel", data={"reason": "Store closed the request"}).status_code == 302
    assert order.status.value == "Cancelled"
    assert app.container.dashboard.navigation_counts()["pending"] == before - 1
    assert any(item.title == "Order cancelled" for item in app.container.notifications.list_all())


def test_completed_order_return_increases_stock_and_records_received_movement(client):
    app, _ = client
    order = app.container.orders.get(4)
    product = app.container.inventory.get(order.lines[0].product_id)
    before = product.stock
    app.container.orders.create_return(order.id, "Maya Chen")
    assert product.stock == before + order.lines[0].quantity
    movement = app.container.movements.history(product.id)[-1]
    assert movement.type == "Received"
    assert movement.reference == f"RETURN-{order.number}"


def test_dashboard_open_badge_excludes_completed_and_cancelled(client):
    app, _ = client
    initial = app.container.dashboard.navigation_counts()["pending"]
    app.container.orders.cancel(1, "Duplicate store request")
    assert app.container.dashboard.navigation_counts()["pending"] == initial - 1
    app.container.orders.complete(3, "Maya Chen")
    assert app.container.dashboard.navigation_counts()["pending"] == initial - 2


def test_session_state_persists_between_app_instances(monkeypatch, tmp_path):
    session_path = tmp_path / "session_state.json"
    monkeypatch.setenv("WIMS_SESSION_PATH", str(session_path))

    app = create_app()
    product = app.container.inventory.get(1)
    product.stock = 42
    app.container.inventory.save(product)

    restarted = create_app()
    assert restarted.container.inventory.get(1).stock == 42
