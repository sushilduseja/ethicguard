import streamlit as st
from transformers import pipeline
import logging

class EthicsAnalysisAgent:
    def __init__(self):
        self.analyzer = st.cache_resource(self._load_model)()
        
    def _load_model(self):
        """Load and cache the model"""
        try:
            return pipeline(
                "zero-shot-classification",  # Changed to zero-shot classification
                model="facebook/bart-large-mnli",  # More reliable for classification
                device="cpu"
            )
        except Exception as e:
            logging.error(f"Model loading failed: {e}")
            return None
    
    def analyze_results(self, bias_results, pii_results, metrics=None):
        """Generate analysis using classification approach"""
        if not self.analyzer:
            return self._generate_fallback_response(bias_results, pii_results)
            
        try:
            # Analyze bias severity
            bias_labels = ["severe bias", "moderate bias", "no significant bias"]
            bias_result = self.analyzer(bias_results, candidate_labels=bias_labels)
            
            # Analyze privacy concerns
            privacy_labels = ["critical privacy issue", "moderate privacy concern", "no privacy risk"]
            privacy_result = self.analyzer(pii_results, candidate_labels=privacy_labels)
            
            # Generate structured response
            response = self._format_analysis(
                bias_label=bias_result['labels'][0],
                bias_score=bias_result['scores'][0],
                privacy_label=privacy_result['labels'][0],
                privacy_score=privacy_result['scores'][0],
                bias_results=bias_results,
                pii_results=pii_results
            )
            
            return response
            
        except Exception as e:
            logging.error(f"Analysis failed: {e}")
            return self._generate_fallback_response(bias_results, pii_results)
    
    def _format_analysis(self, bias_label, bias_score, privacy_label, 
                        privacy_score, bias_results, pii_results):
        """Format analysis results into a structured response"""
        priority = "High" if bias_score > 0.7 or privacy_score > 0.7 else "Medium" if bias_score > 0.4 or privacy_score > 0.4 else "Low"
        
        return f"""Analysis Results:

1. Main ethical concerns:
   - Bias Assessment: {bias_label.title()} (Confidence: {bias_score:.2%})
   - Privacy Risk: {privacy_label.title()} (Confidence: {privacy_score:.2%})

2. Recommended actions:
   {'- Immediate review of bias patterns in the data' if 'severe' in bias_label else '- Monitor bias metrics' if 'moderate' in bias_label else '- Continue standard bias monitoring'}
   {'- Urgent privacy protection measures needed' if 'critical' in privacy_label else '- Review privacy safeguards' if 'moderate' in privacy_label else '- Maintain current privacy measures'}

3. Priority Level: {priority}

Details:
{bias_results}
{pii_results}
"""
    
    def _generate_fallback_response(self, bias_results, pii_results):
        """Generate a basic response when model fails"""
        has_bias = "bias detected" in bias_results.lower()
        has_pii = "pii detected" in pii_results.lower()
        
        return f"""Analysis Results:

1. Main ethical concerns:
   - {'Bias detected in the data' if has_bias else 'No significant bias detected'}
   - {'Privacy concerns identified' if has_pii else 'No privacy issues found'}

2. Recommended actions:
   - {'Review and address bias patterns' if has_bias else 'Continue monitoring'}
   - {'Implement data protection measures' if has_pii else 'Maintain privacy standards'}

3. Priority Level: {'High' if has_bias or has_pii else 'Low'}
"""
