import pandas as pd
import numpy as np

class DataAgent:
    def assess(self, data):
        """Assess bias in input data using demographic parity"""
        try:
            if data.empty:
                return {
                    'score': 0,
                    'rating': '❌ Error',
                    'message': "No data provided"
                }
            
            protected = data['protected_attribute']
            target = data['target']
            prediction = data['prediction']
            
            # Calculate rates
            group_0_mask = protected == 0
            group_1_mask = protected == 1
            
            if not any(group_0_mask) or not any(group_1_mask):
                return {
                    'score': 0,
                    'rating': '❌ Error',
                    'message': "Missing data for one or more groups"
                }
            
            group_0_target = target[group_0_mask].mean()
            group_1_target = target[group_1_mask].mean()
            
            # Calculate bias metrics
            disparity = abs(group_0_target - group_1_target)
            score = 1 - disparity
            
            rating = '✅ Low' if score > 0.8 else '⚠️ Moderate' if score > 0.6 else '❌ High'
            
            return {
                'score': float(score),  # Ensure score is a native float
                'rating': rating,
                'message': f"Bias Rating: {rating}\nGroup 0 Rate: {group_0_target:.2f}\nGroup 1 Rate: {group_1_target:.2f}"
            }
        except Exception as e:
            return {
                'score': 0,
                'rating': '❌ Error',
                'message': f"Error in analysis: {str(e)}"
            }
