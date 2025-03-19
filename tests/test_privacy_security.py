import pytest
import pandas as pd
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from modules.privacy_security import check_pii

@pytest.fixture
def pii_data():
    """Create test data with PII"""
    return pd.DataFrame({
        'email': ['user@example.com', 'test@test.com'],
        'phone': ['123-456-7890', '(555) 123-4567'],
        'ssn': ['123-45-6789', '987-65-4321'],
        'credit_card': ['4111-1111-1111-1111', '5555-5555-5555-5555'],
        'text': ['Normal text', 'More text']
    })

def test_detect_email(pii_data):
    """Test email detection"""
    result = check_pii(pii_data)
    assert "email" in result.lower()

def test_detect_phone(pii_data):
    """Test phone number detection"""
    result = check_pii(pii_data)
    assert "phone" in result.lower()

def test_detect_ssn(pii_data):
    """Test SSN detection"""
    result = check_pii(pii_data)
    assert "ssn" in result.lower()

def test_detect_credit_card(pii_data):
    """Test credit card detection"""
    result = check_pii(pii_data)
    assert "credit_card" in result.lower()

def test_clean_data():
    """Test data without PII"""
    clean_data = pd.DataFrame({
        'name': ['John', 'Jane'],
        'age': [25, 30],
        'score': [0.8, 0.9]
    })
    result = check_pii(clean_data)
    assert "No PII detected" in result
