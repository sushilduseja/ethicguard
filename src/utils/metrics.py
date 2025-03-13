import numpy as np

def calculate_group_metrics(data, group_col, target_col):
    """Calculate basic metrics for different groups"""
    metrics = {}
    unique_groups = data[group_col].unique()
    
    if not all(g in unique_groups for g in [0, 1]):
        return None  # Indicate missing groups
        
    for group in [0, 1]:
        group_data = data[data[group_col] == group]
        metrics[group] = {
            'size': len(group_data),
            'positive_rate': float(group_data[target_col].mean()) if len(group_data) > 0 else 0
        }
    return metrics

def format_metrics(metrics):
    """Format metrics for display"""
    if metrics is None:
        return {
            'disparity': 1.0,  # Maximum disparity when groups are missing
            'group_0_rate': 0,
            'group_1_rate': 0,
            'error': 'Missing required groups (0 and 1)'
        }
    
    return {
        'disparity': abs(metrics[0]['positive_rate'] - metrics[1]['positive_rate']),
        'group_0_rate': metrics[0]['positive_rate'],
        'group_1_rate': metrics[1]['positive_rate']
    }
