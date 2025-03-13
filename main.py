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

st.set_page_config(page_title="EthicGuard", layout="wide", initial_sidebar_state="expanded")

# Move How to Use to sidebar for cleaner main interface
with st.sidebar:
    st.title("📚 Guide")
    st.markdown("""
    ### How to Use EthicGuard
    
    1. **Enter Sample Data**
       - Include both reference (0) and protected (1) groups
       - Add actual outcomes and model predictions
    
    2. **Add Documentation**
       - Describe model purpose
       - Explain data sources
       - List known limitations
    
    3. **Review Results**
       - Check bias score
       - Evaluate fairness metrics
       - Verify documentation completeness
    
    ### Example: Loan Approval Model
    | Group | Description |
    |-------|-------------|
    | 0 | Male applicants |
    | 1 | Female applicants |
    
    | Outcome | Meaning |
    |---------|---------|
    | 0 | Loan Denied |
    | 1 | Loan Approved |
    """)

# Main content
st.title("🛡️ EthicGuard")
st.subheader("AI Ethics Assessment Platform")

with st.form("assessment_form"):
    tab1, tab2 = st.tabs(["📊 Data Input", "📝 Documentation"])
    
    with tab1:
        st.subheader("Sample Data Input")
        rows = st.number_input("Number of samples", 2, 10, 3)
        
        data = []
        group_0_count = 0
        group_1_count = 0
        
        # Group selection grid
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
        
        # Show group balance after data entry
        st.write("---")
        st.markdown("### Group Balance")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Reference Group (0)", group_0_count)
        with col2:
            st.metric("Protected Group (1)", group_1_count)
            
        if group_0_count == 0 and group_1_count == 0:
            st.info("💡 Start entering data above")
        elif group_0_count == 0 or group_1_count == 0:
            st.warning("⚠️ Please include data from both groups!")
        else:
            st.success(f"✅ Data distribution: {group_0_count} reference, {group_1_count} protected")
    
    with tab2:
        st.info("💡 Model Documentation Guidelines")
        doc_cols = st.columns([1, 2])
        with doc_cols[0]:
            st.markdown("""
            **Required Sections:**
            1. Purpose
            2. Data Sources
            3. Limitations
            """)
        with doc_cols[1]:
            doc_text = st.text_area(
                "Documentation",
                height=200,
                placeholder="Purpose: Loan approval prediction\nData: Historical applications 2020-2022\nLimitations: Limited rural data"
            )
    
    submitted = st.form_submit_button("🔍 Analyze Ethics")

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
            
            # Display results in a more organized way
            st.markdown("### 📊 Assessment Results")
            metric_cols = st.columns(3)
            
            with metric_cols[0]:
                st.info("**Bias Analysis**")
                if bias_result and 'score' in bias_result:
                    st.metric("Bias Score", f"{bias_result['score']:.2f}", bias_result.get('rating', ''))
                    st.write(bias_result['message'])
                else:
                    st.error("Invalid bias analysis result")
            
            with metric_cols[1]:
                st.info("**Fairness Evaluation**")
                if fair_result and 'score' in fair_result:
                    st.metric("Fairness Score", f"{fair_result['score']:.2f}", fair_result.get('rating', ''))
                    st.write(fair_result['message'])
                else:
                    st.error("Invalid fairness analysis result")
            
            with metric_cols[2]:
                st.info("**Documentation Review**")
                if doc_result and 'score' in doc_result:
                    st.metric("Compliance Score", f"{doc_result['score']:.2f}", doc_result.get('rating', ''))
                    st.write(doc_result['message'])
                else:
                    st.error("Invalid documentation analysis result")

            if all(result.get('score', 0) > 0.6 for result in [bias_result, fair_result, doc_result]):
                st.success("✅ Model meets ethical guidelines!")
            else:
                st.warning("⚠️ Some aspects need review. Check details above.")
            logging.info("Assessment completed successfully")
            
        except Exception as e:
            st.error(f"Error during analysis: {str(e)}\nPlease check your input data and try again.")
            logging.error(f"General error: {str(e)}")
            import traceback
            logging.error(f"Traceback: {traceback.format_exc()}")
