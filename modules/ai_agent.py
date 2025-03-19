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
                "text-generation",
                model="facebook/opt-125m",  # Lighter model, ~125M parameters
                max_length=200,
                device="cpu"
            )
        except Exception as e:
            logging.error(f"Model loading failed: {e}")
            return None
    
    def analyze_results(self, bias_results, pii_results, metrics=None):
        """Generate analysis using a lightweight HuggingFace model"""
        if not self.analyzer:
            return "AI analysis unavailable. Using basic analysis instead."
            
        try:
            prompt = f"""Analyze ethics assessment:
            {bias_results}
            {pii_results}
            Key concerns and recommendations:"""
            
            result = self.analyzer(
                prompt,
                max_new_tokens=100,
                do_sample=True,
                temperature=0.7,
                num_return_sequences=1
            )
            
            return result[0]['generated_text'].split("Key concerns and recommendations:")[1].strip()
        except Exception as e:
            logging.error(f"Analysis failed: {e}")
            return f"Analysis error. Raw results:\nBias: {bias_results}\nPII: {pii_results}"
