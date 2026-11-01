import re
from datetime import datetime

def validate_employee_record(record, allowed_departments):
    """
    Validates a raw employee record against schema rules and corporate policies.
    Returns a tuple: (is_valid: bool, errors: list)
    """
    errors = []

    # 1. Check required fields
    required_fields = ["employee_id", "first_name", "last_name", "department", "start_date"]
    for field in required_fields:
        if not record.get(field):
            errors.append(f"Missing required field: {field}")

    # If basic fields are missing, return immediately
    if errors:
        return False, errors

    # 2. Validate Employee ID format (e.g., EMP1001)
    emp_id = record.get("employee_id", "")
    if not re.match(r"^EMP\d{4}$", emp_id):
        errors.append(f"Invalid Employee ID format: '{emp_id}'. Must match EMP####.")

    # 3. Validate Department Authorization
    dept = record.get("department", "")
    if allowed_departments and dept not in allowed_departments:
        errors.append(f"Unauthorized Department: '{dept}'. Allowed: {allowed_departments}")

    # 4. Validate Start Date format (YYYY-MM-DD)
    start_date = record.get("start_date", "")
    try:
        datetime.strptime(start_date, "%Y-%m-%d")
    except ValueError:
        errors.append(f"Invalid Start Date format: '{start_date}'. Must be YYYY-MM-DD.")

    is_valid = len(errors) == 0
    return is_valid, errors
