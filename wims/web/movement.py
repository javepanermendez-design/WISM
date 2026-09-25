"""Stock movement blueprint."""
from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for
from .auth import login_required

movement_bp = Blueprint("movement", __name__)


@movement_bp.get("/movements")
@login_required
def movements_view():
    return render_template("movements.html", movements=current_app.container.movements.history(reference=request.args.get("reference")), products=current_app.container.inventory.list())


@movement_bp.route("/movements/adjust", methods=["GET", "POST"])
@login_required
def adjust_stock():
    if request.method == "POST":
        user = current_app.container.auth.current_user(session["user_id"])
        current_app.container.movements.adjust(int(request.form["product_id"]), int(request.form["quantity"]), request.form["reason"], user.name)
        flash("Stock adjustment recorded in the grocery movement log.", "success")
        return redirect(url_for("movements_view"))
    return render_template("movement_adjust.html", products=current_app.container.inventory.list())
