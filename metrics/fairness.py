import numpy as np
from sklearn.metrics import accuracy_score
import sys
import os

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.utils import calculate_group_metrics, format_metrics

def assess_fairness(y_true, y_pred, protected, bias_result=None):
    """Calculate fairness metrics, considering bias"""
    try:
        # Input validation
        if len(y_true) == 0 or len(y_pred) == 0 or len(protected) == 0:
            return {
                'score': 0,
                'rating': '❌ Error',
                'message': "Empty data provided"
            }

        # Convert inputs to numpy arrays
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)
        protected = np.array(protected)

        # Get masks for each group
        group_0_mask = protected == 0
        group_1_mask = protected == 1

        # Validate group sizes
        group_0_size = np.sum(group_0_mask)
        group_1_size = np.sum(group_1_mask)

        if group_0_size == 0 or group_1_size == 0:
            return {
                'score': 0,
                'rating': '❌ Error',
                'message': f"Insufficient samples in groups (Group 0: {group_0_size}, Group 1: {group_1_size})"
            }

        # Safe accuracy calculation
        def safe_accuracy(true, pred):
            if len(true) == 0:
                return np.nan
            return accuracy_score(true, pred)

        # Safe TPR calculation
        def safe_tpr(true, pred, mask):
            if not np.any(mask):
                return np.nan
            
            true_positives = true[mask] == 1
            if not np.any(true_positives):
                return np.nan
            
            if len(pred[mask][true_positives]) == 0:
                return np.nan
            
            return np.mean(pred[mask][true_positives])

        # Calculate accuracies
        acc_0 = safe_accuracy(y_true[group_0_mask], y_pred[group_0_mask])
        acc_1 = safe_accuracy(y_true[group_1_mask], y_pred[group_1_mask])

        # Calculate TPRs
        tpr_0 = safe_tpr(y_true, y_pred, group_0_mask)
        tpr_1 = safe_tpr(y_true, y_pred, group_1_mask)

        # Handle NaN values
        if np.isnan(acc_0) or np.isnan(acc_1) or np.isnan(tpr_0) or np.isnan(tpr_1):
            return {
                'score': 0,
                'rating': '❌ Error',
                'message': "Unable to calculate metrics for one or more groups"
            }

        # Calculate fairness metrics
        acc_diff = abs(acc_0 - acc_1) if not (np.isnan(acc_0) or np.isnan(acc_1)) else 0
        tpr_diff = abs(tpr_0 - tpr_1) if not (np.isnan(tpr_0) or np.isnan(tpr_1)) else 0

        # Overall fairness score (avoiding division by zero)
        fairness_score = 1 - np.mean([acc_diff, tpr_diff])
        rating = '✅ Fair' if fairness_score > 0.8 else '⚠️ Review' if fairness_score > 0.6 else '❌ Unfair'

        return {
            'score': float(fairness_score),  # Convert from numpy to native float
            'rating': rating,
            'details': {
                'accuracy_0': float(acc_0),
                'accuracy_1': float(acc_1),
                'tpr_0': float(tpr_0),
                'tpr_1': float(tpr_1),
                'group_0_size': int(group_0_size),
                'group_1_size': int(group_1_size)
            },
            'message': (f"Fairness Rating: {rating}\n"
                       f"Group 0 (n={group_0_size}): Acc={acc_0:.2f}, TPR={tpr_0:.2f}\n"
                       f"Group 1 (n={group_1_size}): Acc={acc_1:.2f}, TPR={tpr_1:.2f}")
        }
    except Exception as e:
        return {
            'score': 0,
            'rating': '❌ Error',
            'message': f"Error in fairness analysis: {str(e)}"
        }
