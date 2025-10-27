from flask import Blueprint, render_template
from app.models.database_models import Project

projects = Blueprint("projects", __name__)

@projects.route("/")
def projects_page():
    projects = Project.query.order_by(Project.created_at.asc()).all()
    return render_template("projects.html", projects=projects)

@projects.route("/<int:project_id>")
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template("project_detail.html", project=project)
