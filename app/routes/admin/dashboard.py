from flask import render_template, jsonify, current_app
from flask_login import login_required
from app.models.user import User
from app.models.contact_message import ContactMessage
from app.models.project import Project
from app.models.timeline_event import TimelineEvent
from app.models.current_status import CurrentStatus
from app.models.certificate import Certificate
from .bp import admin_bp
import os

@admin_bp.route("/")
@login_required
def dashboard():
    cv_path = os.path.join(current_app.root_path, "static", "cv", "cv.pdf")
    return render_template(
        "admin/dashboard.html",
        user_count=User.query.count(),
        message_count=ContactMessage.query.count(),
        project_count=Project.query.count(),
        timeline_count=TimelineEvent.query.count(),
        status=CurrentStatus.query.filter_by(is_active=True).first(),
        cv_exists=os.path.exists(cv_path),
        certificate_count=Certificate.query.count()
    )


@admin_bp.route("/stats")
@login_required
def stats():
    return jsonify({
        "user_count": User.query.count(),
        "message_count": ContactMessage.query.count(),
        "project_count": Project.query.count(),
        "timeline_count": TimelineEvent.query.count()
    })