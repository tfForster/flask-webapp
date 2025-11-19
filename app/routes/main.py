from flask import Blueprint, render_template
from app.models.database_models import Project

main = Blueprint("main", __name__)

@main.route("/")
def home():
    projects = Project.query.order_by(Project.created_at.desc()).limit(3).all()
    return render_template("index.html", projects=projects)

