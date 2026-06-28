import re
import uuid

class RoomNotAvailableError(Exception): pass
class InvalidDateError(Exception): pass
class GuestNotFoundError(Exception): pass

def format_currency(amount: float) -> str:
    return f"${amount:,.2f}"

def validate_email(email: str) -> bool:
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

def validate_phone(phone: str) -> bool:
    return phone.isdigit() and len(phone) >= 10

def generate_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"
