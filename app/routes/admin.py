from flask import Blueprint, render_template, redirect, url_for, flash, abort, request, session
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.database_models import ContactMessage, Project
import os, uuid
from werkzeug.utils import secure_filename
from flask import jsonify, current_app

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
    project_count = Project.query.count()
    return render_template("admin/dashboard.html", user_count=user_count, message_count=message_count, project_count=project_count)

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
    return redirect(url_for("admin.contact_requests"))

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
    project_count = Project.query.count()
    return jsonify({
        "user_count": user_count,
        "message_count": message_count,
        "project_count": project_count
    })


# projects pages
@admin_bp.route("/projects")
@login_required
def admin_projects():
    sort = request.args.get("sort", "newest")  # default: newest
    if sort == "oldest":
        projects = Project.query.order_by(Project.id.asc()).all()
    else:
        projects = Project.query.order_by(Project.id.desc()).all()
    return render_template("admin/projects.html", projects=projects, sort=sort)


@admin_bp.route("/project/new", methods=["GET", "POST"])
@login_required
def new_project():
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["description"]
        tech = request.form["tech_stack"]
        github = request.form["github_url"]
        live = request.form["live_url"]

        # Bildverarbeitung
        image_file = request.files.get("image")
        image_filename = None
        if image_file and allowed_file(image_file.filename):
            ext = image_file.filename.rsplit('.', 1)[1].lower()
            filename = f"{uuid.uuid4().hex}.{ext}"  # eindeutiger Name
            image_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            image_file.save(image_path)
            image_filename = filename

        project = Project(
            title=title,
            description=desc,
            tech_stack=tech,
            github_url=github,
            live_url=live,
            image=image_filename
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
        # Textfelder übernehmen
        project.title = request.form["title"]
        project.description = request.form["description"]
        project.tech_stack = request.form["tech_stack"]
        project.github_url = request.form["github_url"]
        project.live_url = request.form["live_url"]

        # === BILDDATEI HANDLING ===
        if "image" in request.files:
            file = request.files["image"]

            # Wenn ein neues Bild gewählt wurde
            if file and file.filename.strip() != "":
                filename = secure_filename(file.filename)
                upload_folder = os.path.join(current_app.static_folder, "uploads")

                # Ordner erstellen falls nicht vorhanden
                os.makedirs(upload_folder, exist_ok=True)

                # Datei speichern
                file_path = os.path.join(upload_folder, filename)
                file.save(file_path)

                # Dateiname in DB speichern
                project.image = filename

        # Änderungen speichern
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
    sort = request.form.get("sort", "newest")
    session["project_sort"] = sort  # für die öffentliche Seite speichern
    flash("Sortierung aktualisiert.", "success")
    return redirect(url_for("admin.admin_projects"))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
