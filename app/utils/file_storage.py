import os
import uuid

UPLOAD_DIR = "app/uploads/profile_images"

os.makedirs(UPLOAD_DIR, exist_ok=True)


def save_profile_image(file) -> str:
    file_extension = file.filename.split(".")[-1]

    file_name = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, file_name)

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    return file_path