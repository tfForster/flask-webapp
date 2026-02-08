from flask import render_template, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models.contact_message import ContactMessage
from .bp import admin_bp

@admin_bp.route("/contacts")
@login_required
def contact_requests():
    messages = ContactMessage.query.order_by(ContactMessage.id.desc()).all()
    return render_template("admin/contact_requests.html", messages=messages)

@admin_bp.route("/contact/<int:message_id>")
@login_required
def contact_detail(message_id):
    msg = ContactMessage.query.get_or_404(message_id)
    return render_template("admin/contact_detail.html", message=msg)

@admin_bp.route("/contacts/delete/<int:message_id>")
@login_required
def delete_contact_request(message_id):
    msg = ContactMessage.query.get_or_404(message_id)
    db.session.delete(msg)
    db.session.commit()
    flash("Nachricht gelöscht.", "success")
    return redirect(url_for("admin.contact_requests"))
