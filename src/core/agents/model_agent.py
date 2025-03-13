import numpy as np
from sklearn.metrics import accuracy_score

class ModelAgent:
    def assess(self, model_details):
        """Analyze model fairness using accuracy and prediction parity"""
        try:
            y_true = np.array(model_details['y_true'])
            y_pred = np.array(model_details['y_pred'])
            sensitive = np.array(model_details['sensitive_features'])

            # Validate group sizes
            group_0 = sensitive == 0
            group_1 = sensitive == 1
            
            if not np.any(group_0) or not np.any(group_1):
                return {
                    "score": 0,
                    "rating": '❌ Error',
                    "message": f"Insufficient data: Group 0: {np.sum(group_0)}, Group 1: {np.sum(group_1)} samples"
                }

            # Safe calculation functions
            def safe_metric(func, true, pred):
                try:
                    if len(true) == 0 or len(pred) == 0:
                        return 0.0
                    return float(func(true, pred))
                except:
                    return 0.0

            def safe_tpr(true, pred):
                try:
                    if len(true) == 0 or len(pred) == 0:
                        return 0.0
                    positives = true == 1
                    if not np.any(positives):
                        return 0.0
                    return float(np.mean(pred[positives]))
                except:
                    return 0.0

            # Calculate metrics with safety checks
            acc_0 = safe_metric(accuracy_score, y_true[group_0], y_pred[group_0])
            acc_1 = safe_metric(accuracy_score, y_true[group_1], y_pred[group_1])
            tpr_0 = safe_tpr(y_true[group_0], y_pred[group_0])
            tpr_1 = safe_tpr(y_true[group_1], y_pred[group_1])

            # Calculate disparities
            acc_diff = abs(acc_0 - acc_1)
            tpr_diff = abs(tpr_0 - tpr_1)

            # Calculate overall fairness score
            fairness_score = float(1 - np.mean([acc_diff, tpr_diff]))
            fairness_score = max(0.0, min(1.0, fairness_score))  # Clamp between 0 and 1

            rating = '✅ Fair' if fairness_score > 0.8 else '⚠️ Review' if fairness_score > 0.6 else '❌ Unfair'

            return {
                "score": fairness_score,
                "rating": rating,
                "details": {
                    "accuracy_0": acc_0,
                    "accuracy_1": acc_1,
                    "tpr_0": tpr_0,
                    "tpr_1": tpr_1,
                    "group_0_size": int(np.sum(group_0)),
                    "group_1_size": int(np.sum(group_1))
                },
                "message": (
                    f"Fairness Analysis Results:\n\n"
                    f"Reference Group (n={np.sum(group_0)}):\n"
                    f"• Accuracy: {acc_0:.2f} ({acc_0*100:.0f}% correct)\n"
                    f"• Success Rate: {tpr_0:.2f} ({tpr_0*100:.0f}% positive outcomes)\n\n"
                    f"Protected Group (n={np.sum(group_1)}):\n"
                    f"• Accuracy: {acc_1:.2f} ({acc_1*100:.0f}% correct)\n"
                    f"• Success Rate: {tpr_1:.2f} ({tpr_1*100:.0f}% positive outcomes)\n\n"
                    f"Fairness Assessment: {rating}"
                )
            }
        except Exception as e:
            return {
                "score": 0,
                "rating": '❌ Error',
                "message": f"Error in fairness analysis: {str(e)}"
            }
