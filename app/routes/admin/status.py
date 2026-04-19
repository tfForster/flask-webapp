from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required
from app import db
from app.models.current_status import CurrentStatus
from .bp import admin_bp


@admin_bp.route("/status")
@login_required
def admin_status():
    entries = CurrentStatus.query.order_by(CurrentStatus.updated_at.desc()).all()
    return render_template("admin/status.html", entries=entries)


@admin_bp.route("/status/new", methods=["GET", "POST"])
@login_required
def new_status():
    if request.method == "POST":
        # Alle anderen deaktivieren wenn neuer aktiv gesetzt wird
        if request.form.get("is_active"):
            CurrentStatus.query.update({"is_active": False})

        entry = CurrentStatus(
            title=request.form["title"],
            description=request.form.get("description", ""),
            tech_stack=request.form.get("tech_stack", ""),
            is_active=bool(request.form.get("is_active")),
        )
        db.session.add(entry)
        db.session.commit()
        flash("Status erstellt.", "success")
        return redirect(url_for("admin.admin_status"))

    return render_template("admin/status_form.html")


@admin_bp.route("/status/edit/<int:status_id>", methods=["GET", "POST"])
@login_required
def edit_status(status_id):
    entry = CurrentStatus.query.get_or_404(status_id)

    if request.method == "POST":
        # Wenn dieser aktiv gesetzt wird, alle anderen deaktivieren
        if request.form.get("is_active"):
            CurrentStatus.query.update({"is_active": False})

        entry.title = request.form["title"]
        entry.description = request.form.get("description", "")
        entry.tech_stack = request.form.get("tech_stack", "")
        entry.is_active = bool(request.form.get("is_active"))
        db.session.commit()
        flash("Status aktualisiert.", "success")
        return redirect(url_for("admin.admin_status"))

    return render_template("admin/status_form.html", entry=entry)


@admin_bp.route("/status/delete/<int:status_id>", methods=["POST"])
@login_required
def delete_status(status_id):
    entry = CurrentStatus.query.get_or_404(status_id)
    db.session.delete(entry)
    db.session.commit()
    flash("Status gelöscht.", "success")
    return redirect(url_for("admin.admin_status"))