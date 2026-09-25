"""Dashboard blueprint."""
from flask import Blueprint, current_app, render_template
from .auth import login_required

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.get("/")
@login_required
def dashboard():
    return render_template("dashboard.html", zone_names=current_app.container.zone_names, **current_app.container.dashboard.summary())
