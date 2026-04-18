from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required
from app import db
from app.models.timeline_event import TimelineEvent
from .bp import admin_bp


@admin_bp.route("/timeline")
@login_required
def admin_timeline():
    events = TimelineEvent.query.order_by(TimelineEvent.order.asc()).all()
    return render_template("admin/timeline.html", events=events)


@admin_bp.route("/timeline/new", methods=["GET", "POST"])
@login_required
def new_timeline_event():
    if request.method == "POST":
        event = TimelineEvent(
            year=request.form["year"],
            title=request.form["title"],
            subtitle=request.form.get("subtitle", ""),
            is_current=bool(request.form.get("is_current")),
            order=int(request.form.get("order", 0)),
        )
        db.session.add(event)
        db.session.commit()
        flash("Eintrag erstellt.", "success")
        return redirect(url_for("admin.admin_timeline"))

    return render_template("admin/timeline_form.html")


@admin_bp.route("/timeline/edit/<int:event_id>", methods=["GET", "POST"])
@login_required
def edit_timeline_event(event_id):
    event = TimelineEvent.query.get_or_404(event_id)

    if request.method == "POST":
        event.year = request.form["year"]
        event.title = request.form["title"]
        event.subtitle = request.form.get("subtitle", "")
        event.is_current = bool(request.form.get("is_current"))
        event.order = int(request.form.get("order", 0))
        db.session.commit()
        flash("Eintrag aktualisiert.", "success")
        return redirect(url_for("admin.admin_timeline"))

    return render_template("admin/timeline_form.html", event=event)


@admin_bp.route("/timeline/delete/<int:event_id>", methods=["POST"])
@login_required
def delete_timeline_event(event_id):
    event = TimelineEvent.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash("Eintrag gelöscht.", "success")
    return redirect(url_for("admin.admin_timeline"))