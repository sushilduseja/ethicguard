import streamlit as st
from modules.input_handler import load_data
from modules.bias_detection import detect_bias, create_bias_chart
from modules.privacy_security import check_pii
from modules.report_generator import generate_report
from modules.ai_agent import EthicsAnalysisAgent
import pandas as pd
import os

@st.cache_resource
def get_ai_agent():
    return EthicsAnalysisAgent()

# UI Configuration
st.set_page_config(page_title="EthicGuard", layout="wide")
st.title("EthicGuard - AI Ethics Assessment")
st.markdown("Assess your AI systems for ethical concerns with ease.")

# Initialize AI agent
ai_agent = get_ai_agent()

# Data Upload
st.subheader("Step 1: Upload Your Data")
data = load_data()

if data is not None:
    st.success("Data loaded successfully!")
    st.write("Preview:", data.head())
    
    # Column Selection
    st.subheader("Step 2: Configure Assessment")
    
    # Add model prediction columns if available
    prediction_col = None
    label_col = None
    if 'predictions' in data.columns or 'labels' in data.columns:
        st.write("### Model Evaluation")
        col3, col4 = st.columns(2)
        with col3:
            prediction_col = st.selectbox(
                "Model Predictions",
                data.columns,
                help="Column containing model predictions"
            )
        with col4:
            label_col = st.selectbox(
                "True Labels",
                data.columns,
                help="Column containing true labels"
            )
    
    # Get numeric columns for outcome selection
    numeric_columns = data.select_dtypes(include=['int64', 'float64']).columns
    
    col1, col2 = st.columns(2)
    with col1:
        sensitive_attr = st.selectbox(
            "Sensitive Attribute",
            data.columns,
            help="Select the attribute to check for bias (e.g., gender, race)"
        )
    with col2:
        if len(numeric_columns) > 0:
            outcome_col = st.selectbox(
                "Outcome Column",
                numeric_columns,
                help="Select the numeric column to analyze (e.g., score, salary)"
            )
        else:
            st.error("No numeric columns found in the dataset. The outcome column must be numeric.")
            st.stop()
    
    # Run Assessment
    if st.button("Run Assessment", use_container_width=True, help="Click to analyze data for bias and privacy concerns"):
        with st.spinner("Running comprehensive analysis..."):
            # Run all analyses in parallel for better performance
            col1, col2 = st.columns(2)
            
            with col1:
                bias_result, group_means = detect_bias(data, sensitive_attr, outcome_col)
                if not bias_result.startswith("Error"):
                    st.success("✅ Bias analysis complete")
                    
            with col2:
                pii_result = check_pii(data)
                st.success("✅ Privacy check complete")
            
            # Get AI insights and generate report
            analysis = ai_agent.analyze_results(bias_result, pii_result)
            report = generate_report(bias_result, pii_result)
            
            # Show results in tabs for better organization
            tab1, tab2, tab3 = st.tabs(["📊 Visualization", "🤖 AI Analysis", "📝 Report"])
            
            with tab1:
                fig = create_bias_chart(group_means, sensitive_attr, outcome_col)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                st.write(analysis)
            
            with tab3:
                st.markdown("### Full Report")
                st.markdown("```\n" + report + "\n```")
                st.download_button(
                    "📥 Download Report",
                    report,
                    "ethicguard_report.txt",
                    use_container_width=True
                )
else:
    st.info("Please upload a CSV file to begin.")