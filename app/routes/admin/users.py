from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from .bp import admin_bp

@admin_bp.route("/users")
@login_required
def users():
    return render_template("admin/users.html", users=User.query.all())

@admin_bp.route("/user/<int:user_id>", methods=["GET", "POST"])
@login_required
def user_detail(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == "POST":
        user.username = request.form.get("username", user.username)
        user.email = request.form.get("email", user.email)
        db.session.commit()
        flash("Benutzerdaten aktualisiert.", "success")

    return render_template("admin/user_detail.html", user=user)

@admin_bp.route("/user/delete/<int:user_id>")
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    if user.id == current_user.id:
        flash("Du kannst dich nicht selbst löschen!", "danger")
        return redirect(url_for("admin.users"))

    db.session.delete(user)
    db.session.commit()
    flash("Benutzer gelöscht.", "success")
    return redirect(url_for("admin.users"))

@admin_bp.route("/user/toggle_role/<int:user_id>")
@login_required
def toggle_role(user_id):
    user = User.query.get_or_404(user_id)
    user.role = "admin" if user.role == "user" else "user"
    db.session.commit()
    flash(f"Rolle geändert zu {user.role}", "info")
    return redirect(url_for("admin.users"))
