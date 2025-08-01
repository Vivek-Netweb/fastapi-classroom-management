import os
import uuid
from fastapi import UploadFile
from app.utils.api_response import error_response

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".jpg"}
MAX_FILE_SIZE_MB = 5  # Max 5 MB

async def save_file(file : UploadFile, upload_dir : str, base_url : str) -> str:

    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        return error_response(message=f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}", status_code=400)

    
    # Ensure directory exists
    os.makedirs(upload_dir, exist_ok=True)

    # Read file content for size validation
    file_content = await file.read()
    file_size_mb = len(file_content) / (1024 * 1024)  # Convert to MB

    if file_size_mb > MAX_FILE_SIZE_MB:
        return error_response(message=f"File size exceeds {MAX_FILE_SIZE_MB} MB limit", status_code=400)
    
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(upload_dir, unique_filename).replace("\\", "/")

    with open(file_path, "wb") as f:
        f.write(file_content)

    public_url = f"{base_url}/{file_path}".replace("\\", "/")

    print(public_url)
    return file_path,public_url