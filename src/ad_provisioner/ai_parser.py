import re
import json

def parse_natural_language_request(text_prompt: str) -> dict:
    """
    Parses unstructured natural language text into a structured employee dictionary
    matching the schema expected by validation and lifecycle engines.
    Example prompt: 'Hire John Doe in Engineering, employee ID EMP1050, starting 2026-11-15.'
    """
    record = {
        "employee_id": "",
        "first_name": "",
        "last_name": "",
        "department": "",
        "role": "Standard User",
        "start_date": "",
        "action": "CREATE"
    }
    
    if not text_prompt or not isinstance(text_prompt, str):
        return record

    # Extract Employee ID (e.g., EMP1050)
    emp_id_match = re.search(r'(EMP\d{4})', text_prompt, re.IGNORECASE)
    if emp_id_match:
        record["employee_id"] = emp_id_match.group(1).upper()

    # Extract Names (e.g., "John Doe")
    name_match = re.search(r'(?:hire|onboard|add)\s+([A-Z][a-z]+)\s+([A-Z][a-z]+)', text_prompt, re.IGNORECASE)
    if name_match:
        record["first_name"] = name_match.group(1)
        record["last_name"] = name_match.group(2)

    # Extract Department (e.g., Engineering, Finance, IT, HR)
    depts = ["Engineering", "Finance", "IT", "HR", "Product Management", "Security"]
    for dept in depts:
        if dept.lower() in text_prompt.lower():
            record["department"] = dept
            break

    # Extract Date (YYYY-MM-DD format)
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', text_prompt)
    if date_match:
        record["start_date"] = date_match.group(1)

    return record
