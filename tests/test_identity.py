import pytest
from ad_provisioner.identity import generate_username, generate_email, generate_secure_password

def test_generate_username():
    username = generate_username("Sarah", "Jenkins", "corp.local")
    assert username == "sjenkins"

def test_generate_email():
    email = generate_email("sjenkins", "corp.local")
    assert email == "sjenkins@corp.local"

def test_generate_secure_password():
    pwd = generate_secure_password(length=16)
    assert len(pwd) == 16
    assert any(c.isupper() for c in pwd)
    assert any(c.islower() for c in pwd)
    assert any(c.isdigit() for c in pwd)
