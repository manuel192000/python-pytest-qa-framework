"""Small validation helpers used as the system under test for the unit-test examples."""

import re

_EMAIL_RE = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")
MIN_PASSWORD_LENGTH = 8


def is_valid_email(value: str) -> bool:
    """Return True when value looks like an email address (local@domain.tld)."""
    return _EMAIL_RE.fullmatch(value) is not None


def password_errors(password: str) -> list[str]:
    """Return a list of rule codes the password breaks; empty means valid."""
    errors: list[str] = []
    if len(password) < MIN_PASSWORD_LENGTH:
        errors.append("too_short")
    if not any(char.isdigit() for char in password):
        errors.append("missing_digit")
    if not any(char.isupper() for char in password):
        errors.append("missing_uppercase")
    return errors
