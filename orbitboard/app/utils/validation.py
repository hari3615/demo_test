# app/utils/validation.py
import re

def validate_email(email: str) -> bool:
    # A simple regex for email validation
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None
