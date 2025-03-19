import pytest
import pandas as pd
import numpy as np
import os
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

@pytest.fixture(scope="session")
def test_data_dir():
    """Return path to test data directory"""
    return os.path.join(os.path.dirname(__file__), "data")

@pytest.fixture
def sample_dataset(test_data_dir):
    """Load sample dataset for testing"""
    return pd.read_csv(os.path.join(test_data_dir, "test_dataset.csv"))

@pytest.fixture
def large_dataset():
    """Create a larger synthetic dataset for performance testing"""
    np.random.seed(42)
    n_samples = 1000
    
    return pd.DataFrame({
        'gender': np.random.choice(['M', 'F'], n_samples),
        'race': np.random.choice(['White', 'Black', 'Asian', 'Hispanic'], n_samples),
        'age': np.random.randint(20, 60, n_samples),
        'score': np.random.normal(0.75, 0.15, n_samples),
        'salary': np.random.normal(85000, 15000, n_samples)
    })
