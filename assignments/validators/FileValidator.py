import os

from rest_framework.exceptions import ValidationError

ALLOWED_EXTENSIONS = [
    '.pdf',
    '.docx',
    '.xlsx',
    '.csv',
    '.doc',
    '.xls'
]

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

def validate_file(file):
    # Check file extension
    ext = os.path.splitext(file.name)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(f"Unsupported file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}")

    if file.size > MAX_FILE_SIZE:
        raise ValidationError(f"File size exceeds the limit of {MAX_FILE_SIZE / (1024 * 1024)} MB.")
