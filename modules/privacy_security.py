import pandas as pd
import re

def check_pii(data: pd.DataFrame) -> str:
    """Check for potential PII in the dataset."""
    pii_patterns = {
        'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
        'credit_card': r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'
    }
    
    pii_found = {}
    for column in data.columns:
        column_data = data[column].astype(str)
        for pii_type, pattern in pii_patterns.items():
            matches = column_data.str.contains(pattern, regex=True, na=False)
            if matches.any():
                if pii_type not in pii_found:
                    pii_found[pii_type] = []
                pii_found[pii_type].append(column)
    
    if pii_found:
        findings = [f"{k} in {', '.join(v)}" for k, v in pii_found.items()]
        return f"⚠️ Potential PII detected: {'; '.join(findings)}"
    return "✅ No PII detected in the dataset."