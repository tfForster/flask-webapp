from flask import render_template, jsonify
from flask_login import login_required
from app.models.user import User
from app.models.contact_message import ContactMessage
from app.models.project import Project
from .bp import admin_bp


@admin_bp.route("/")
@login_required
def dashboard():
    return render_template(
        "admin/dashboard.html",
        user_count=User.query.count(),
        message_count=ContactMessage.query.count(),
        project_count=Project.query.count()
    )

@admin_bp.route("/stats")
@login_required
def stats():
    return jsonify({
        "user_count": User.query.count(),
        "message_count": ContactMessage.query.count(),
        "project_count": Project.query.count()
    })
