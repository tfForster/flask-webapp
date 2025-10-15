from flask import Blueprint, render_template, request, flash, redirect, url_for

contact = Blueprint("contact", __name__)

@contact.route("/", methods=["GET", "POST"])
def contact_page():
    from app import db
    from app.models.database_models import ContactMessage


    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        # Einfache Validierung
        if not name or not email or not message:
            flash("Bitte fülle alle Felder aus.", "danger")
        else:
            # Daten in der Datenbank speichern
            new_message = ContactMessage(name=name, email=email, message=message)
            db.session.add(new_message)
            db.session.commit()


            
            flash("nachricht erfolgreich gesendet! Vielen Dank :)", "sucess")
            return redirect(url_for("contact.contact_page"))
        
    return render_template("contact.html")