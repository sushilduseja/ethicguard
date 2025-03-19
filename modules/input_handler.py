import streamlit as st
import pandas as pd
import os

def load_sample_datasets():
    """Load available sample datasets"""
    samples = {
        "HR Analytics": "hr_hiring_decisions.csv",
        "Loan Applications": "loan_applications.csv",
        "Healthcare Outcomes": "patient_treatment.csv",
        "Education Scores": "student_performance.csv"
    }
    return samples

def load_data():
    """Load data from CSV file or use sample data"""
    st.write("Choose your data source:")
    
    data_source = st.radio(
        "Input Method",
        ["Upload CSV", "Use Sample Data"],
        horizontal=True
    )
    
    if data_source == "Upload CSV":
        uploaded_file = st.file_uploader("Upload CSV file", type="csv")
        if uploaded_file is not None:
            try:
                return pd.read_csv(uploaded_file)
            except Exception as e:
                st.error(f"Error loading file: {e}")
                return None
    else:
        samples = load_sample_datasets()
        selected_sample = st.selectbox(
            "Select a sample dataset",
            list(samples.keys()),
            help="Choose a pre-built dataset to explore"
        )
        
        try:
            file_path = os.path.join("sample_data", samples[selected_sample])
            return pd.read_csv(file_path)
        except Exception as e:
            st.error(f"Error loading sample data: {e}")
            return None
    
    return None
