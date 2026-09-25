"""WIMS application package."""
from flask import Flask, flash, redirect, render_template, request, session, url_for

from .config import Config
from .container import Container
from .domain.exceptions import WimsError


def create_app(config_class: type[Config] = Config) -> Flask:
    """Build and configure a WIMS Flask application."""
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(config_class)
    app.container = Container.build()

    from .web.auth import auth_bp
    from .web.dashboard import dashboard_bp
    from .web.inventory import inventory_bp
    from .web.receiving import receiving_bp
    from .web.orders import orders_bp
    from .web.movement import movement_bp
    from .web.reports import reports_bp

    for blueprint in (auth_bp, dashboard_bp, inventory_bp, receiving_bp, orders_bp, movement_bp, reports_bp):
        app.register_blueprint(blueprint)

    # Keep the prototype's short endpoint names valid for unchanged templates.
    for rule in list(app.url_map.iter_rules()):
        if "." not in rule.endpoint:
            continue
        short_name = rule.endpoint.rsplit(".", 1)[-1]
        if short_name in app.view_functions or short_name == "product_form":
            continue
        methods = rule.methods - {"HEAD", "OPTIONS"}
        app.add_url_rule(rule.rule, endpoint=short_name, view_func=app.view_functions[rule.endpoint], methods=methods)

    product_form_view = app.view_functions["inventory.product_form"]
    app.add_url_rule("/inventory/new", endpoint="product_form", view_func=product_form_view, methods=["GET", "POST"])
    app.add_url_rule("/inventory/<int:product_id>/edit", endpoint="product_form", view_func=product_form_view, methods=["GET", "POST"])

    @app.context_processor
    def inject_globals() -> dict[str, object]:
        user = app.container.auth.current_user(session.get("user_id"))
        summary = app.container.dashboard.navigation_counts()
        return {"current_user": user, "notifications": app.container.notifications.list_all(), "nav_counts": summary}

    @app.errorhandler(WimsError)
    def handle_wims_error(error: WimsError):
        flash(error.message, "danger")
        return redirect(request.referrer or url_for("dashboard.dashboard"))

    @app.errorhandler(404)
    def handle_not_found(error):
        return render_template("404.html"), 404

    return app
