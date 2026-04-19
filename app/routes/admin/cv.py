import os
from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required
from .bp import admin_bp
from .utils import handle_cv_upload


@admin_bp.route("/cv", methods=["GET", "POST"])
@login_required
def admin_cv():
    cv_path = os.path.join(current_app.root_path, "static", "cv", "cv.pdf")
    cv_exists = os.path.exists(cv_path)

    if request.method == "POST":
        result = handle_cv_upload()
        if result:
            flash("CV erfolgreich hochgeladen.", "success")
        else:
            flash("Fehler – bitte eine PDF-Datei hochladen.", "danger")
        return redirect(url_for("admin.admin_cv"))

    return render_template("admin/cv.html", cv_exists=cv_exists)