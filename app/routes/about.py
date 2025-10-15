from flask import Blueprint, render_template

about = Blueprint("about", __name__)

@about.route("/")
def about_page():
    return render_template("about.html")
