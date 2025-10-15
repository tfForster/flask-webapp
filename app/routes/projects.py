from flask import Blueprint, render_template

projects = Blueprint("projects", __name__)

@projects.route("/")
def projects_page():
    project_list = [
        {"title": "Flask Portfolio", "desc": "Meine persönliche Website mit Flask", "tech": "Flask, Bootstrap"},
        {"title": "Spring Boot API", "desc": "REST API für Fahrgemeinschafts-App", "tech": "Java, Spring Boot"},
        {"title": "ShareYourRide", "desc": "Frontend-Projekt auf Azure-VM", "tech": "HTML, CSS, JS"},
    ]
    return render_template("projects.html", projects=project_list)