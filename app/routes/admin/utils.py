import os, uuid
from flask import request, current_app
from werkzeug.utils import secure_filename

def allowed_file(filename):
    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in current_app.config["ALLOWED_EXTENSIONS"]

def handle_image_upload():
    image_file = request.files.get("image")
    if not image_file or image_file.filename == "":
        return None

    if not allowed_file(image_file.filename):
        return None

    ext = image_file.filename.rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    image_file.save(path)
    return filename

def handle_cv_upload():
    cv_file = request.files.get("cv")
    if not cv_file or cv_file.filename == "":
        return None

    if not cv_file.filename.lower().endswith(".pdf"):
        return None

    cv_folder = os.path.join(current_app.root_path, "static", "cv")
    os.makedirs(cv_folder, exist_ok=True)

    path = os.path.join(cv_folder, "cv.pdf")
    cv_file.save(path)
    return True