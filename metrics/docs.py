import numpy as np
import sys
import os

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.utils import calculate_group_metrics, format_metrics

def assess_documentation(text, bias_result=None, fair_result=None):
    """Simple documentation completeness check, considering bias and fairness"""
    required = {
        'purpose': ['purpose', 'goal', 'objective'],
        'data': ['data', 'dataset', 'input'],
        'limitations': ['limitation', 'constraint', 'bias']
    }
    
    text = text.lower()
    scores = {}
    found = []
    
    for section, keywords in required.items():
        has_section = any(k in text for k in keywords)
        scores[section] = 1.0 if has_section else 0.0
        if has_section:
            found.append(section)
    
    score = sum(scores.values()) / len(required)
    rating = '✅ Complete' if score > 0.8 else '⚠️ Partial' if score > 0.5 else '❌ Incomplete'
    
    # Adjust score based on bias and fairness
    if bias_result and bias_result['score'] < 0.6:
        score -= 0.2  # Penalize for high bias
    if fair_result and fair_result['score'] < 0.6:
        score -= 0.2  # Penalize for low fairness

    return {
        'score': score,
        'rating': rating,
        'found_sections': found,
        'message': f"Documentation Rating: {rating}\nFound sections: {', '.join(found)}"
    }
