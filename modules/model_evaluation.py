import numpy as np
from sklearn.metrics import confusion_matrix, classification_report
import pandas as pd

def evaluate_model_fairness(predictions, labels, sensitive_attributes):
    """
    Evaluate ML model fairness across different demographic groups
    """
    results = {}
    
    for group in sensitive_attributes.unique():
        group_mask = sensitive_attributes == group
        group_preds = predictions[group_mask]
        group_labels = labels[group_mask]
        
        # Calculate fairness metrics
        tn, fp, fn, tp = confusion_matrix(group_labels, group_preds).ravel()
        
        results[group] = {
            'true_positive_rate': tp / (tp + fn) if (tp + fn) > 0 else 0,
            'false_positive_rate': fp / (fp + tn) if (fp + tn) > 0 else 0,
            'accuracy': (tp + tn) / (tp + tn + fp + fn),
            'sample_size': len(group_labels)
        }
    
    return pd.DataFrame(results).T

def calculate_disparate_impact(predictions, sensitive_attributes, positive_label=1):
    """
    Calculate disparate impact ratio between demographic groups
    """
    groups = sensitive_attributes.unique()
    group_probs = {}
    
    for group in groups:
        group_mask = sensitive_attributes == group
        group_preds = predictions[group_mask]
        group_probs[group] = (group_preds == positive_label).mean()
    
    # Calculate ratios between groups
    ratios = {}
    for i in range(len(groups)):
        for j in range(i + 1, len(groups)):
            ratio = group_probs[groups[i]] / group_probs[groups[j]]
            ratios[f"{groups[i]} vs {groups[j]}"] = ratio
    
    return ratios
