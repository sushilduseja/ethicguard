import pandas as pd
import plotly.express as px
from scipy import stats

def detect_bias(data, sensitive_attr, outcome_col):
    """Detect potential bias and return group means for visualization."""
    if sensitive_attr not in data.columns or outcome_col not in data.columns:
        return "Error: Sensitive attribute or outcome column not found.", None
    
    # Check if outcome column is numeric
    if not pd.api.types.is_numeric_dtype(data[outcome_col]):
        return f"Error: Outcome column '{outcome_col}' must be numeric.", None
    
    try:
        # Calculate mean outcome for each group
        group_means = data.groupby(sensitive_attr)[outcome_col].mean().to_dict()
        
        # Group data for statistical testing
        groups = data[sensitive_attr].unique()
        outcomes = {group: data[data[sensitive_attr] == group][outcome_col].dropna() for group in groups}
        
        # Perform t-tests between groups to detect significant differences
        p_values = {}
        for i in range(len(groups)):
            for j in range(i + 1, len(groups)):
                if len(outcomes[groups[i]]) > 1 and len(outcomes[groups[j]]) > 1:
                    t_stat, p_val = stats.ttest_ind(outcomes[groups[i]], outcomes[groups[j]])
                    p_values[f"{groups[i]} vs {groups[j]}"] = p_val
        
        # Identify pairs with significant differences (p < 0.05)
        biased_pairs = [pair for pair, p_val in p_values.items() if p_val < 0.05]
        bias_result = (f"Potential bias detected between: {', '.join(biased_pairs)}" if biased_pairs 
                       else "No significant bias detected.")
        
        return bias_result, group_means
    except Exception as e:
        return f"Error during bias detection: {str(e)}", None

def create_bias_chart(group_means, sensitive_attr, outcome_col):
    """Create a Plotly bar chart for group means."""
    if group_means is None:
        return None
    
    # Convert group means to a DataFrame for Plotly
    df = pd.DataFrame(list(group_means.items()), columns=[sensitive_attr, 'Mean Outcome'])
    
    # Create a bar chart using Plotly Express
    fig = px.bar(
        df,
        x=sensitive_attr,
        y='Mean Outcome',
        title=f'Mean {outcome_col} by {sensitive_attr}',
        labels={'Mean Outcome': f'Mean {outcome_col}', sensitive_attr: sensitive_attr}
    )
    
    # Customize the layout for clarity
    fig.update_layout(
        xaxis_title=sensitive_attr,
        yaxis_title=f'Mean {outcome_col}',
        bargap=0.2  # Add a small gap between bars
    )
    
    return fig