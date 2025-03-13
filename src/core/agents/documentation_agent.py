from transformers import pipeline
import numpy as np

class DocumentationAgent:
    def assess(self, documentation, bias_result=None, fair_result=None):
        """Simple documentation completeness check"""
        if documentation == "[Describe your model's purpose]" or documentation.strip() == "":
            return {
                "score": 0,
                "rating": '❌ Error',
                "message": "Please provide actual documentation"
            }
            
        required_sections = {
            'purpose': ['purpose', 'objective', 'goal'],
            'data': ['data', 'dataset', 'collection'],
            'limitations': ['limitation', 'constraint', 'bias', 'issue']
        }
        
        try:
            doc_lower = documentation.lower()
            scores = {}
            found_keywords = []
            
            for section, keywords in required_sections.items():
                section_found = False
                for keyword in keywords:
                    if keyword in doc_lower:
                        section_found = True
                        found_keywords.append(keyword)
                        break
                scores[section] = 1.0 if section_found else 0.0
            
            compliance_score = sum(scores.values()) / len(required_sections)
            
            # Adjust score based on bias and fairness results
            if bias_result and bias_result['score'] < 0.6:
                compliance_score = max(0, compliance_score - 0.2)  # Prevent negative scores
            if fair_result and fair_result['score'] < 0.6:
                compliance_score = max(0, compliance_score - 0.2)  # Prevent negative scores
            
            return {
                "score": compliance_score,
                "rating": '✅ Complete' if compliance_score > 0.8 else '⚠️ Partial' if compliance_score > 0.5 else '❌ Incomplete',
                "section_scores": scores,
                "found_keywords": found_keywords,
                "message": f"Found {sum(scores.values())}/{len(required_sections)} required sections.\nKeywords found: {', '.join(found_keywords)}"
            }
        except Exception as e:
            return {
                "score": 0,
                "rating": '❌ Error',
                "message": f"Error in analysis: {str(e)}"
            }