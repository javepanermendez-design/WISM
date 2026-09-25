"""Orders and picking blueprint."""
from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, session, url_for
from .auth import login_required

orders_bp = Blueprint("orders", __name__)


@orders_bp.get("/orders")
@login_required
def orders_view():
    status = request.args.get("status", "Active")
    query = request.args.get("q", "")
    date_from = request.args.get("date_from", "")
    date_to = request.args.get("date_to", "")
    service = current_app.container.orders
    completed_id = request.args.get("completed", type=int)
    completed_order = service.get(completed_id) if completed_id else None
    return render_template("orders/index.html", orders=service.list(status, query, date_from, date_to), all_orders=service.list("All"), selected_status=status, query=query, date_from=date_from, date_to=date_to, completed_order=completed_order)


@orders_bp.route("/orders/<int:order_id>", methods=["GET", "POST"])
@login_required
def order_detail(order_id):
    service = current_app.container.orders
    try:
        order = service.get(order_id)
    except ValueError:
        abort(404)
    if request.method == "POST":
        action = request.form.get("action")
        if action == "picking":
            service.start_picking(order_id)
        elif action == "pick":
            service.pick(order_id, int(request.form.get("line_index", 0)))
        elif action == "unpick":
            service.unpick(order_id, int(request.form.get("line_index", 0)))
        elif action == "ready":
            service.mark_ready(order_id)
        elif action == "complete":
            user = current_app.container.auth.current_user(session["user_id"])
            service.complete(order_id, user.name)
            completed = service.get(order_id)
            flash(f"{completed.number} completed by {completed.completed_by}. Released {sum(line.quantity for line in completed.lines)} grocery units.", "success")
            return redirect(url_for("orders_view", completed=order_id))
        order = service.get(order_id)
        flash(f"{order.number} is now {order.status.value.lower()}.", "success")
        return redirect(url_for("order_detail", order_id=order_id))
    return render_template("orders/detail.html", order=order, lines=order.lines)


@orders_bp.post("/orders/<int:order_id>/cancel")
@login_required
def cancel_order(order_id):
    current_app.container.orders.cancel(order_id, request.form.get("reason", ""))
    flash("Order cancelled. No stock was deducted.", "success")
    return redirect(url_for("orders_view", status="Cancelled"))


@orders_bp.post("/orders/<int:order_id>/return")
@login_required
def create_return(order_id):
    user = current_app.container.auth.current_user(session["user_id"])
    current_app.container.orders.create_return(order_id, user.name)
    flash("Return received. Original release movements remain unchanged.", "success")
    return redirect(url_for("order_detail", order_id=order_id))
