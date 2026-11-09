import re

class UserValidator:
    def __init__(self, config):
        self.config = config

    def validate_user(self, row):
        errors = []
        
        if not row.get('FirstName') or not row.get('LastName'):
            errors.append("Missing mandatory first or last name.")
            
        email = row.get('Email', '')
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            errors.append(f"Invalid email format: {email}")
            
        return errors
