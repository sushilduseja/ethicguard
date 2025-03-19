import streamlit as st
import pandas as pd

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
        # Sample data for demonstration
        return pd.DataFrame({
            'gender': ['M', 'F', 'M', 'F', 'M', 'F'],
            'age': [25, 30, 35, 40, 45, 50],
            'score': [0.8, 0.6, 0.9, 0.7, 0.85, 0.65]
        })
    
    return None
