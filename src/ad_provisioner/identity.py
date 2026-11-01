import secrets
import string

def generate_username(first_name, last_name, domain="corp.local"):
    """Generates a standardized username: first initial + last name (e.g., sjenkins)."""
    clean_first = "".join(c for c in first_name if c.isalpha()).lower()
    clean_last = "".join(c for c in last_name if c.isalpha()).lower()
    if not clean_first or not clean_last:
        return "unknown.user"
    return f"{clean_first[0]}{clean_last}"

def generate_email(username, domain="corp.local"):
    """Generates a corporate email address from the username and domain."""
    return f"{username}@{domain}"

def generate_secure_password(length=14):
    """Generates a cryptographically secure temporary password meeting complexity rules."""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    while True:
        password = "".join(secrets.choice(alphabet) for _ in range(length))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and any(c.isdigit() for c in password)
                and any(c in "!@#$%^&*()-_=+" for c in password)):
            return password
