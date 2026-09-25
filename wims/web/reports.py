"""Reports and notifications blueprint."""
from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from .auth import login_required

reports_bp = Blueprint("reports", __name__)


@reports_bp.get("/reports")
@login_required
def reports():
    selected_report = request.args.get("report", "inventory")
    products = current_app.container.inventory.list()
    movements = current_app.container.movements.history()
    orders = current_app.container.orders.list("All")
    report_data = {
        "products": [{
            "name": product.name,
            "sku": product.sku,
            "stock": product.stock,
            "min_stock": product.min_stock,
            "status": product.status.value,
            "category": product.category,
            "unit": product.unit,
        } for product in products],
        "movements": [{
            "reference": movement.reference,
            "type": movement.type,
            "delta": movement.delta,
            "date": movement.created.isoformat(),
        } for movement in movements],
        "orders": [{
            "number": order.number,
            "customer": order.customer,
            "status": order.status.value,
            "progress": order.progress,
            "created": order.created.isoformat() if hasattr(order.created, "isoformat") else str(order.created),
        } for order in orders],
    }
    return render_template("reports.html", products=products, movements=movements, orders=orders, selected_report=selected_report, report_data=report_data)


@reports_bp.post("/notifications/read")
@login_required
def mark_notifications():
    current_app.container.notifications.mark_all_read()
    flash("All notifications marked as read.", "success")
    return redirect(request.referrer or url_for("reports"))
