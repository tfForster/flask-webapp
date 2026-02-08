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
