import os, uuid
from flask import render_template, redirect, url_for, request, flash, current_app
from flask_login import login_required
from datetime import datetime
from app import db
from app.models.certificate import Certificate
from .bp import admin_bp


def handle_certificate_upload():
    f = request.files.get("file")
    if not f or f.filename == "":
        return None
    if not f.filename.lower().endswith(".pdf"):
        return None

    cert_folder = os.path.join(current_app.root_path, "static", "certificates")
    os.makedirs(cert_folder, exist_ok=True)

    filename = f"{uuid.uuid4().hex}.pdf"
    f.save(os.path.join(cert_folder, filename))
    return filename


@admin_bp.route("/certificates")
@login_required
def admin_certificates():
    certs = Certificate.query.order_by(Certificate.order.asc()).all()
    return render_template("admin/certificates.html", certs=certs)


@admin_bp.route("/certificate/new", methods=["GET", "POST"])
@login_required
def new_certificate():
    if request.method == "POST":
        filename = handle_certificate_upload()
        if not filename:
            flash("Bitte eine gültige PDF-Datei hochladen.", "danger")
            return redirect(request.url)

        date_str = request.form.get("date")
        date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None

        cert = Certificate(
            title=request.form["title"],
            issuer=request.form.get("issuer", ""),
            date=date,
            file=filename,
            type=request.form.get("type", "Zertifikat"),
            is_public=bool(request.form.get("is_public")),
            order=int(request.form.get("order", 0)),
        )
        db.session.add(cert)
        db.session.commit()
        flash("Zertifikat hochgeladen.", "success")
        return redirect(url_for("admin.admin_certificates"))

    return render_template("admin/certificate_form.html")


@admin_bp.route("/certificate/edit/<int:cert_id>", methods=["GET", "POST"])
@login_required
def edit_certificate(cert_id):
    cert = Certificate.query.get_or_404(cert_id)

    if request.method == "POST":
        date_str = request.form.get("date")
        cert.date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None
        cert.title = request.form["title"]
        cert.issuer = request.form.get("issuer", "")
        cert.type = request.form.get("type", "Zertifikat")
        cert.is_public = bool(request.form.get("is_public"))
        cert.order = int(request.form.get("order", 0))

        new_file = handle_certificate_upload()
        if new_file:
            # alte Datei löschen
            old_path = os.path.join(current_app.root_path, "static", "certificates", cert.file)
            if os.path.exists(old_path):
                os.remove(old_path)
            cert.file = new_file

        db.session.commit()
        flash("Zertifikat aktualisiert.", "success")
        return redirect(url_for("admin.admin_certificates"))

    return render_template("admin/certificate_form.html", cert=cert)


@admin_bp.route("/certificate/delete/<int:cert_id>", methods=["POST"])
@login_required
def delete_certificate(cert_id):
    cert = Certificate.query.get_or_404(cert_id)

    # PDF löschen
    path = os.path.join(current_app.root_path, "static", "certificates", cert.file)
    if os.path.exists(path):
        os.remove(path)

    db.session.delete(cert)
    db.session.commit()
    flash("Zertifikat gelöscht.", "success")
    return redirect(url_for("admin.admin_certificates"))