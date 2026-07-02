import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}


def allowed_file(filename):
    return (
        isinstance(filename, str)
        and "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def save_upload(file, upload_folder=UPLOAD_FOLDER):
    if file is None or not allowed_file(file.filename):
        return {"success": False, "message": "Unsupported file format."}

    filename = secure_filename(file.filename)
    if not filename:
        return {"success": False, "message": "Invalid file name."}

    os.makedirs(upload_folder, exist_ok=True)
    path = os.path.join(upload_folder, filename)
    file.save(path)

    return {"success": True, "path": path}
