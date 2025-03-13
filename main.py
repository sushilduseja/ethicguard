import streamlit as st
import pandas as pd
import os
import sys
import logging
from datetime import datetime
from src.config import setup_logging

# Setup logging
setup_logging()

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from metrics import bias, fairness, docs
from src.core.agents.data_agent import DataAgent
from src.core.agents.model_agent import ModelAgent
from src.core.agents.documentation_agent import DocumentationAgent

st.set_page_config(page_title="EthicGuard", layout="wide")
st.title("🛡️ EthicGuard - AI Ethics Assessment")

with st.expander("ℹ️ How to use"):
    st.write("""
    ### Welcome to EthicGuard!
    
    This tool helps you check if your AI model is treating different groups fairly.
    
    #### Input Guide:
    1. **Protected Group**: Choose which group each data point belongs to
       - 0 = Reference Group (e.g., Male)
       - 1 = Protected Group (e.g., Female)
    
    2. **Actual Outcome**: The true result that occurred
       - 0 = Negative (e.g., Loan Denied)
       - 1 = Positive (e.g., Loan Approved)
    
    3. **Model Prediction**: What your model predicted
       - 0 = Negative Prediction
       - 1 = Positive Prediction
    
    #### Example Use Case:
    If you're analyzing a loan approval system:
    - Protected Group: Gender (0=Male, 1=Female)
    - Actual: Loan Status (0=Denied, 1=Approved)
    - Prediction: Model's Decision (0=Deny, 1=Approve)
    """)

with st.form("assessment_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Sample Data Input")
        rows = st.number_input("Number of data points to analyze", 2, 10, 3)
        
        # Add group balance tracking
        st.info("💡 For meaningful analysis, include data from both groups:")
        
        data = []
        group_0_count = 0
        group_1_count = 0
        
        # Create two columns for group selection
        group_col1, group_col2 = st.columns(2)
        
        with group_col1:
            st.markdown("**Reference Group (0)**")
            st.write(f"Current count: {group_0_count}")
            
        with group_col2:
            st.markdown("**Protected Group (1)**")
            st.write(f"Current count: {group_1_count}")
        
        for i in range(rows):
            c1, c2, c3 = st.columns(3)
            with c1:
                protected = st.selectbox(
                    f"Group #{i+1}",
                    options=[0, 1],
                    help="0 = Reference Group (e.g., Male)\n1 = Protected Group (e.g., Female)",
                    key=f"group_{i}"
                )
                # Update counts
                if protected == 0:
                    group_0_count += 1
                else:
                    group_1_count += 1
                    
            with c2:
                actual = st.selectbox(
                    f"Actual #{i+1}",
                    options=[0, 1],
                    help="0 = Negative (e.g., Denied)\n1 = Positive (e.g., Approved)",
                    key=f"actual_{i}"
                )
            with c3:
                predicted = st.selectbox(
                    f"Prediction #{i+1}",
                    options=[0, 1],
                    help="0 = Negative\n1 = Positive",
                    key=f"pred_{i}"
                )
            data.append([protected, actual, predicted])
        
        # Show warning if groups are unbalanced
        if group_0_count == 0 or group_1_count == 0:
            st.warning("⚠️ Please include data from both groups for meaningful analysis!")
        else:
            st.success(f"✅ Data distribution: {group_0_count} reference vs {group_1_count} protected")
    
    with col2:
        st.subheader("Model Documentation")
        st.info("💡 Describe your model, covering these key areas:")
        st.markdown("""
        1. **Purpose**: What is your model trying to predict?
        2. **Data**: What data was used to train it?
        3. **Limitations**: What are its known limitations?
        """)
        doc_text = st.text_area(
            "Documentation",
            height=200,
            placeholder="""Example:
Purpose: This model predicts loan approval likelihood
Data: Historical loan applications from 2020-2022
Limitations: Limited data from rural areas"""
        )
    
    submitted = st.form_submit_button("Analyze Ethics")

if submitted:
    # Validate input data
    if not data:
        st.error("Please provide at least 2 data points")
        logging.warning("Assessment attempted with no data")
    elif group_0_count == 0 or group_1_count == 0:
        st.error("Please include at least one data point from each group")
        logging.warning("Assessment attempted with missing group data")
    else:
        try:
            # Prepare data
            df = pd.DataFrame(data, columns=['protected_attribute', 'target', 'prediction'])
            logging.info(f"Processing dataset with shape: {df.shape}")
            
            # Simulate agent coordination
            data_agent = DataAgent()
            model_agent = ModelAgent()
            doc_agent = DocumentationAgent()
            
            # Data Agent assesses bias
            bias_result = data_agent.assess(df)
            
            # Model Agent assesses fairness
            model_details = {
                'y_true': df['target'].values,
                'y_pred': df['prediction'].values,
                'sensitive_features': df['protected_attribute'].values
            }
            fair_result = model_agent.assess(model_details)  # Remove bias_result
            
            # Documentation Agent assesses documentation
            doc_result = doc_agent.assess(doc_text)  # Remove extra arguments
            
            # Display results
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.header("Data Bias Analysis")
                if bias_result and 'score' in bias_result:
                    st.metric("Bias Score", f"{bias_result['score']:.2f}", bias_result.get('rating', ''))
                    st.write(bias_result['message'])
                else:
                    st.error("Invalid bias analysis result")
            
            with col2:
                st.header("Fairness Analysis")
                if fair_result and 'score' in fair_result:
                    st.metric("Fairness Score", f"{fair_result['score']:.2f}", fair_result.get('rating', ''))
                    st.write(fair_result['message'])
                else:
                    st.error("Invalid fairness analysis result")
            
            with col3:
                st.header("Documentation Analysis")
                if doc_result and 'score' in doc_result:
                    st.metric("Compliance Score", f"{doc_result['score']:.2f}", doc_result.get('rating', ''))
                    st.write(doc_result['message'])
                else:
                    st.error("Invalid documentation analysis result")

            st.success("✅ Assessment Complete!")
            logging.info("Assessment completed successfully")
            
        except Exception as e:
            st.error(f"Error during analysis: {str(e)}\nPlease check your input data and try again.")
            logging.error(f"General error: {str(e)}")
            import traceback
            logging.error(f"Traceback: {traceback.format_exc()}")
