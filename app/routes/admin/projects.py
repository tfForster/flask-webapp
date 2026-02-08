from flask import render_template, redirect, url_for, request, session, current_app
from flask_login import login_required
from app import db
from app.models.project import Project
from .bp import admin_bp
from .utils import handle_image_upload

@admin_bp.route("/projects")
@login_required
def admin_projects():
    sort = request.args.get("sort", "newest")
    order = Project.id.asc() if sort == "oldest" else Project.id.desc()
    projects = Project.query.order_by(order).all()
    return render_template("admin/projects.html", projects=projects, sort=sort)

@admin_bp.route("/project/new", methods=["GET", "POST"])
@login_required
def new_project():
    if request.method == "POST":
        project = Project(
            title=request.form["title"],
            short_description=request.form["short_description"],
            description=request.form["description"],
            tech_stack=request.form["tech_stack"],
            github_url=request.form["github_url"],
            live_url=request.form["live_url"],
            image=handle_image_upload()
        )
        db.session.add(project)
        db.session.commit()
        return redirect(url_for("admin.admin_projects"))

    return render_template("admin/project_form.html")

@admin_bp.route("/project/edit/<int:project_id>", methods=["GET", "POST"])
@login_required
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)

    if request.method == "POST":
        for field in ["title", "short_description", "description", "tech_stack", "github_url", "live_url"]:
            setattr(project, field, request.form[field])

        image = handle_image_upload()
        if image:
            project.image = image

        db.session.commit()
        return redirect(url_for("admin.edit_project", project_id=project.id))

    return render_template("admin/project_form.html", project=project)

@admin_bp.route("/project/delete/<int:project_id>", methods=["POST"])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for("admin.admin_projects"))

@admin_bp.route("/projects/sort", methods=["POST"])
@login_required
def set_project_sort():
    session["project_sort"] = request.form.get("sort", "newest")
    return redirect(url_for("admin.admin_projects"))
