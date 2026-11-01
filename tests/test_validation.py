import pytest
from ad_provisioner.validation import validate_employee_record

def sample_allowed_depts():
    return ["Engineering", "Finance", "IT", "HR"]

def test_valid_employee_record():
    record = {
        "employee_id": "EMP1001",
        "first_name": "Sarah",
        "last_name": "Jenkins",
        "department": "Engineering",
        "role": "Software Engineer",
        "start_date": "2026-11-01",
        "action": "CREATE"
    }
    is_valid, errors = validate_employee_record(record, sample_allowed_depts())
    assert is_valid is True
    assert len(errors) == 0

def test_invalid_employee_id_format():
    record = {
        "employee_id": "INVALID_ID",
        "first_name": "John",
        "last_name": "Doe",
        "department": "IT",
        "role": "SysAdmin",
        "start_date": "2026-11-01",
        "action": "CREATE"
    }
    is_valid, errors = validate_employee_record(record, sample_allowed_depts())
    assert is_valid is False
    assert any("Employee ID" in err for err in errors)

def test_unauthorized_department():
    record = {
        "employee_id": "EMP1002",
        "first_name": "Alice",
        "last_name": "Smith",
        "department": "Marketing",
        "role": "Manager",
        "start_date": "2026-11-01",
        "action": "CREATE"
    }
    is_valid, errors = validate_employee_record(record, sample_allowed_depts())
    assert is_valid is False
    assert any("Department" in err for err in errors)
