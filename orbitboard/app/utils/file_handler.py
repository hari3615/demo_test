"""
app/utils/file_handler.py

Handles file uploads and downloads for task attachments.

SECURITY FINDING (Path Traversal / CWE-22): The `read_attachment` function
builds a file path using user-supplied input with no sanitisation. An attacker
can pass `filename="../../etc/passwd"` to read arbitrary files on the server.
"""
import os
import mimetypes
import logging

logger = logging.getLogger(__name__)

# Base directory where uploaded files are stored
UPLOAD_DIR = "/var/orbitboard/uploads"


def save_upload(filename: str, content: bytes) -> str:
    """Write uploaded bytes to disk and return the stored path."""
    safe_name = os.path.basename(filename)  # strip leading path components
    dest = os.path.join(UPLOAD_DIR, safe_name)
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    with open(dest, "wb") as f:
        f.write(content)
    logger.info(f"Saved upload: {dest}")
    return dest


def read_attachment(filename: str) -> bytes:
    """
    Read an attachment from the upload directory and return its bytes.

    PATH TRAVERSAL BUG (CWE-22): The filename is NOT sanitised before joining
    with UPLOAD_DIR.  An attacker supplying filename='../../etc/passwd' will
    cause this function to read arbitrary files on the host filesystem.

    No os.path.basename() or realpath check is applied here.
    """
    # Vulnerability: unsanitised user input joined directly into a file path
    full_path = os.path.join(UPLOAD_DIR, filename)
    with open(full_path, "rb") as f:
        return f.read()


def get_mime_type(filename: str) -> str:
    mime, _ = mimetypes.guess_type(filename)
    return mime or "application/octet-stream"
