"""Receiving blueprint."""
from datetime import date
from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for
from .auth import login_required
from ..domain.enums import ItemCondition
from ..domain.exceptions import ValidationError

receiving_bp = Blueprint("receiving", __name__)


@receiving_bp.route("/receiving", methods=["GET", "POST"])
@login_required
def receiving():
    step = request.args.get("step", "details")
    service = current_app.container.receiving
    delivery = service.get_expected()
    if request.method == "POST":
        action = request.form.get("action")
        for item in delivery.items:
            quantity = request.form.get(f"quantity_{item.product_id}")
            if quantity is not None:
                try:
                    item.quantity = int(quantity)
                except ValueError as exc:
                    raise ValidationError("Received quantities must be whole numbers.") from exc
        if action == "review":
            return redirect(url_for("receiving", step="review"))
        if action == "confirm":
            try:
                delivery.condition = ItemCondition(request.form.get("condition", ItemCondition.GOOD.value))
            except ValueError as exc:
                raise ValidationError("Choose a valid delivery condition.") from exc
            delivery.notes = request.form.get("notes", "")
            for item in delivery.items:
                product = current_app.container.inventory.get(item.product_id)
                expiry = request.form.get(f"expiry_{item.product_id}", "")
                if product.category in {"Dairy & Frozen", "Canned Goods", "Snacks & Biscuits", "Noodles & Pasta"} and not expiry:
                    raise ValidationError(f"Expiry date is required for {product.name}.")
                if expiry:
                    product.expiry_date = date.fromisoformat(expiry)
            preview = service.confirm(delivery, current_app.container.auth.current_user(session["user_id"]).name)
            flash(f"Receipt confirmed. {sum(after - before for _, before, after in preview)} grocery units are now available.", "success")
            return redirect(url_for("receiving", step="done"))
    suppliers = [item.supplier for item in current_app.container.receiving.deliveries.list()]
    delivery_products = [current_app.container.inventory.get(item.product_id) for item in delivery.items]
    return render_template("receiving.html", step=step, delivery=delivery, delivery_products=delivery_products, suppliers=suppliers)
