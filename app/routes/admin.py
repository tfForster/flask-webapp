from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.database_models import ContactMessage
from flask import jsonify

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.before_request
def restrict_to_admins():
    if not current_user.is_authenticated or not current_user.is_admin():
        abort(403)

@admin_bp.route("/")
@login_required
def dashboard():
    user_count = User.query.count()
    message_count = ContactMessage.query.count()
    return render_template("admin/dashboard.html", user_count=user_count, message_count=message_count)

@admin_bp.route("/users")
@login_required
def users():
    all_users = User.query.all()
    return render_template("admin/users.html", users=all_users)

@admin_bp.route("/user/delete/<int:user_id>")
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("Du kannst dich nicht selbst löschen!", "danger")
        return redirect(url_for("admin.users"))
    
    db.session.delete(user)
    db.session.commit()
    flash("Benutzer wurde gelöscht.", "success")
    return redirect(url_for("admin.users"))
    
@admin_bp.route("/user/toggle_role/<int:user_id>")
@login_required
def toggle_role(user_id):
    user = User.query.get_or_404(user_id)
    user.role = "admin" if user.role == "user" else "user"
    db.session.commit()
    flash(f"Rolle von {user.username} geändert zu: {user.role}", "info")
    return redirect(url_for("admin.users"))

# user detail page
@admin_bp.route("/user/<int:user_id>", methods=["GET", "POST"])
@login_required
def user_detail(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == "POST":
        user.username = request.form.get("username", user.username)
        user.email = request.form.get("email", user.email)
        db.session.commit()
        flash("Benutzerdaten wurden aktualisiert.", "success")
        return redirect(url_for("admin.user_detail", user_id=user.id))

    return render_template("admin/user_detail.html", user=user)


@admin_bp.route("/contacts")
@login_required
def contact_requests():
    messages = ContactMessage.query.order_by(ContactMessage.id.desc()).all()
    return render_template("admin/contact_requests.html", messages=messages)

@admin_bp.route("/contacts/delete/<int:message_id>")
@login_required
def delete_contact_request(message_id):
    msg = ContactMessage.query.get_or_404(message_id)
    db.session.delete(msg)
    db.session.commit()
    flash("Nachricht gelöscht.","success")
    return redirect(url_for("admin.contacts"))

# cotacts detail page
@admin_bp.route("/contact/<int:message_id>")
@login_required
def contact_detail(message_id):
    msg = ContactMessage.query.get_or_404(message_id)
    return render_template("admin/contact_detail.html", message=msg)


# count numbers for admin dashboard
@admin_bp.route("/stats")
@login_required
def stats():
    user_count = User.query.count()
    message_count = ContactMessage.query.count()
    return jsonify({
        "user_count": user_count,
        "message_count": message_count
    })

