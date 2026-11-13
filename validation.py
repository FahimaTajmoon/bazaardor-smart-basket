"""Input validation functions for BazaarDor.

Each function returns the cleaned value if it is valid,
or raises ValueError with a clear message if it is not.
"""

import math
from datetime import datetime


def validate_text(value, field_name):
    """Required text field: must not be empty."""
    value = value.strip()
    if value == "":
        raise ValueError(f"{field_name} cannot be empty.")
    return value


def validate_price(value):
    """Price must be a number greater than zero."""
    try:
        price = float(value)
    except (ValueError, TypeError):
        raise ValueError("Price must be a number.") from None
    if not math.isfinite(price) or price <= 0:
        raise ValueError("Price must be greater than zero.")
    return price


def validate_quantity(value):
    """Quantity must be a number greater than zero."""
    try:
        quantity = float(value)
    except (ValueError, TypeError):
        raise ValueError("Quantity must be a number.") from None
    if not math.isfinite(quantity) or quantity <= 0:
        raise ValueError("Quantity must be greater than zero.")
    return quantity


def validate_date(value):
    """Date must be a real date in YYYY-MM-DD format."""
    try:
        parsed = datetime.strptime(value.strip(), "%Y-%m-%d")
    except ValueError:
        raise ValueError("Date must be like 2026-11-13 (YYYY-MM-DD).") from None
    return parsed.strftime("%Y-%m-%d")


def validate_choice(value, options, field_name):
    """Value must be one of the fixed options (a tuple such as UNITS)."""
    if value not in options:
        raise ValueError(f"{field_name} must be one of: {', '.join(options)}.")
    return value


def validate_unique_id(record_id, used_ids):
    """Record ID must not be empty and must not already exist in the set."""
    record_id = validate_text(record_id, "Record ID").upper()
    if record_id in used_ids:
        raise ValueError(f"Record ID {record_id} already exists.")
    return record_id