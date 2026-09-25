"""Authentication blueprint."""
from datetime import date
from functools import wraps

from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for

from ..domain.exceptions import AuthenticationError

auth_bp = Blueprint("auth", __name__)


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        try:
            user = _container().auth.authenticate(request.form.get("email", "").strip(), request.form.get("password", ""))
            session["user_id"] = user.id
            return redirect(request.args.get("next") or url_for("dashboard"))
        except AuthenticationError as exc:
            error = exc.message
    return render_template("auth/login.html", error=error)


@auth_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user = _container().auth.current_user(session.get("user_id"))
    if user is None:
        return redirect(url_for("login"))

    errors: dict[str, str] = {}
    form = {
        "display_name": user.name,
        "current_password": "",
        "new_password": "",
        "confirm_password": "",
    }

    if request.method == "POST":
        form["display_name"] = (request.form.get("display_name") or "").strip()
        form["current_password"] = request.form.get("current_password") or ""
        form["new_password"] = request.form.get("new_password") or ""
        form["confirm_password"] = request.form.get("confirm_password") or ""

        if not form["display_name"]:
            errors["display_name"] = "Display name is required."

        if form["current_password"] or form["new_password"] or form["confirm_password"]:
            if not form["current_password"]:
                errors["current_password"] = "Current password is required."
            elif form["current_password"] != "warehouse":
                errors["current_password"] = "The current password does not match the demo account."

            if len(form["new_password"]) < 8:
                errors["new_password"] = "Use at least 8 characters."
            if not form["confirm_password"]:
                errors["confirm_password"] = "Please confirm the new password."
            elif form["new_password"] != form["confirm_password"]:
                errors["confirm_password"] = "Passwords do not match."

        if not errors:
            user.name = form["display_name"]
            flash("Profile updated for this demo session. Changes reset on server restart.", "success")
            return redirect(url_for("profile"))

    created_date = getattr(user, "created_at", None) or date.today()
    return render_template(
        "profile.html",
        user=user,
        form=form,
        errors=errors,
        created_date=created_date,
    )


@auth_bp.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


def _container():
    return current_app.container
