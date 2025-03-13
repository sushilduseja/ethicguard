import numpy as np
import sys
import os

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.utils import calculate_group_metrics, format_metrics

def assess_bias(data):
    """Calculate bias metrics"""
    try:
        if len(data) < 2:
            return {
                'score': 0,
                'rating': '❌ Error',
                'message': "Insufficient data for bias analysis (minimum 2 samples required)"
            }
        
        if not all(col in data.columns for col in ['protected_attribute', 'target']):
            return {
                'score': 0,
                'rating': '❌ Error',
                'message': "Missing required columns: protected_attribute, target"
            }
        
        metrics = calculate_group_metrics(data, 'protected_attribute', 'target')
        formatted = format_metrics(metrics)
        
        # Check for empty groups
        if metrics[0]['size'] == 0 or metrics[1]['size'] == 0:
            return {
                'score': 0,
                'rating': '❌ Error',
                'message': f"Missing data for groups:\nGroup 0: {metrics[0]['size']} samples\nGroup 1: {metrics[1]['size']} samples"
            }
        
        score = 1 - formatted['disparity']
        
        if np.isnan(score):
            score = 0
            rating = '❌ Error'
            message = "Unable to calculate bias score due to NaN values"
        else:
            rating = '✅ Low' if score > 0.8 else '⚠️ Moderate' if score > 0.6 else '❌ High'
            message = f"Bias Rating: {rating}\nGroup 0 Rate: {formatted['group_0_rate']:.2f}\nGroup 1 Rate: {formatted['group_1_rate']:.2f}"
        
        return {
            'score': score,
            'rating': rating,
            'details': formatted,
            'message': message
        }
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in bias assessment: {error_details}")  # For dev logs
        return {
            'score': 0,
            'rating': '❌ Error',
            'message': f"Error analyzing bias: {str(e)}\nPlease check data format and try again."
        }
