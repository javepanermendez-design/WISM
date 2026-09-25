"""Inventory blueprint with POST/redirect/GET write flows."""
from datetime import date

from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, url_for

from .auth import login_required
from ..domain.entities import Location, Product
from ..domain.exceptions import DuplicateSkuError, ValidationError

inventory_bp = Blueprint("inventory", __name__)


def _catalog() -> dict[str, list[str]]:
    container = current_app.container
    return {"categories": container.categories, "zones": container.zones, "zone_names": container.zone_names, "suppliers": container.suppliers}


def _form_product(product: Product | None = None) -> Product:
    form = request.form
    expiry = form.get("expiry_date", "").strip()
    return Product(
        id=product.id if product else 0,
        sku=form.get("sku", product.sku if product else "").strip().upper(),
        name=form.get("name", product.name if product else "").strip(),
        category=form.get("category", product.category if product else current_app.container.categories[0]),
        location=Location(form.get("zone", product.zone if product else "A"), form.get("aisle", product.aisle if product else "01"), form.get("bin", product.bin if product else "01")),
        stock=int(form.get("stock", product.stock if product else 0) or 0),
        min_stock=int(form.get("min_stock", product.min_stock if product else 0) or 0),
        max_stock=int(form.get("max_stock", product.max_stock if product else 100) or 0),
        unit=form.get("unit", product.unit if product else "case"),
        supplier=form.get("supplier", product.supplier if product else current_app.container.suppliers[0]),
        price=float(form.get("price", product.price if product else 0) or 0),
        expiry_date=date.fromisoformat(expiry) if expiry else None,
    )


@inventory_bp.get("/inventory")
@login_required
def inventory():
    query, status, zone = request.args.get("q", "").lower(), request.args.get("status", ""), request.args.get("zone", "")
    products = current_app.container.inventory.list(query, status, zone)
    return render_template("inventory/index.html", products=products, query=query, status=status, zone=zone, created_id=request.args.get("created"), updated_id=request.args.get("updated"), **_catalog())


@inventory_bp.route("/inventory/new", methods=["GET", "POST"])
@inventory_bp.route("/inventory/<int:product_id>/edit", methods=["GET", "POST"])
@login_required
def product_form(product_id=None):
    service = current_app.container.inventory
    existing = service.get(product_id) if product_id else None
    if request.method == "POST":
        try:
            product = _form_product(existing)
            saved = service.save(product) if existing else service.create(product)
            flash(f"Product {'updated' if existing else 'added'}: {saved.name}", "success")
            return redirect(url_for("inventory", updated=saved.id) if existing else url_for("inventory", created=saved.id))
        except (ValueError, ValidationError, DuplicateSkuError) as exc:
            error = str(exc) if isinstance(exc, ValueError) else exc.message
            flash(error, "danger")
            existing = _form_product(existing) if not isinstance(exc, ValueError) else existing
            return render_template("inventory/form.html", product=existing, form_error=error, **_catalog()), 422
    return render_template("inventory/form.html", product=existing, **_catalog())


@inventory_bp.get("/inventory/<int:product_id>")
@login_required
def product_detail(product_id):
    product = current_app.container.inventory.get(product_id)
    if not product or product.archived:
        abort(404)
    return render_template("inventory/detail.html", product=product, zone_names=current_app.container.zone_names)


@inventory_bp.post("/inventory/<int:product_id>/delete")
@login_required
def delete_product(product_id):
    product = current_app.container.inventory.get(product_id)
    if not product:
        abort(404)
    current_app.container.inventory.archive(product_id)
    flash(f"Deleted {product.name}::undo=/inventory/{product_id}/restore", "undo")
    return redirect(url_for("inventory"))


@inventory_bp.post("/inventory/<int:product_id>/restore")
@login_required
def restore_product(product_id):
    product = current_app.container.inventory.get(product_id)
    if not product:
        abort(404)
    current_app.container.inventory.restore(product_id)
    flash(f"Restored {product.name}", "success")
    return redirect(url_for("inventory", created=product_id))
