import pytest
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from modules.bias_detection import detect_bias, create_bias_chart

@pytest.fixture
def sample_data():
    """Create sample data for testing"""
    return pd.DataFrame({
        'gender': ['M', 'F', 'M', 'F', 'M'] * 20,
        'race': ['White', 'Black', 'Asian', 'Hispanic', 'White'] * 20,
        'score': [0.9, 0.6, 0.8, 0.7, 0.85] * 20,
        'salary': [100000, 75000, 95000, 80000, 98000] * 20
    })

def test_detect_bias_gender_score(sample_data):
    """Test bias detection with gender and score"""
    result, means = detect_bias(sample_data, 'gender', 'score')
    assert "Potential bias detected" in result
    assert len(means) == 2  # M and F
    assert all(0 <= v <= 1 for v in means.values())

def test_detect_bias_race_salary(sample_data):
    """Test bias detection with race and salary"""
    result, means = detect_bias(sample_data, 'race', 'salary')
    assert "Potential bias detected" in result
    assert len(means) == 4  # White, Black, Asian, Hispanic
    assert all(v > 0 for v in means.values())

def test_invalid_columns():
    """Test error handling for invalid columns"""
    df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    result, means = detect_bias(df, 'C', 'D')
    assert "Error" in result
    assert means is None

def test_create_bias_chart(sample_data):
    """Test bias visualization creation"""
    _, means = detect_bias(sample_data, 'gender', 'score')
    fig = create_bias_chart(means, 'gender', 'score')
    assert fig is not None
    assert fig.data[0].type == 'bar'
