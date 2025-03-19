# EthicGuard

An AI ethics assessment tool that helps identify potential bias, privacy concerns, and fairness issues in your data and AI systems.

## Overview

EthicGuard provides automated analysis of:
- Bias detection across demographic groups
- AI-powered ethics assessment using HuggingFace models
- Model fairness evaluation and disparate impact analysis
- Privacy and PII (Personally Identifiable Information) detection
- Statistical significance testing
- Interactive visualizations of group disparities

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ethicguard.git
cd ethicguard
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Access the web interface at `http://localhost:8501`

3. Choose your data source:
   - Upload a CSV file
   - Use sample data for testing

4. Configure your assessment:
   - Select the sensitive attribute (e.g., gender, race)
   - Choose the outcome column (must be numeric)

5. Review the results:
   - Bias detection analysis
   - Privacy concerns
   - Interactive visualizations
   - Downloadable report

## Project Structure

```
ethicguard/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Project dependencies
│
└── modules/
    ├── ai_agent.py          # AI-powered analysis using HuggingFace
    ├── bias_detection.py    # Statistical bias analysis
    ├── input_handler.py     # Data loading and preprocessing
    ├── model_evaluation.py  # ML model fairness assessment
    ├── privacy_security.py  # PII detection
    └── report_generator.py  # Report generation
```

## Features

### AI-Powered Analysis
- Lightweight text generation model (facebook/opt-125m)
- Automated insights and recommendations
- Fallback mechanisms for reliability

### Bias Detection
- Statistical analysis of outcome differences between groups
- T-test for significance testing
- Interactive visualizations of group disparities
- Comprehensive bias reporting

### Model Fairness Assessment
- True/false positive rate analysis by group
- Disparate impact calculations
- Group-wise accuracy metrics
- Sample size monitoring

### Privacy Analysis
- Detection of common PII patterns:
  - Email addresses
  - Phone numbers
  - Social Security numbers
  - Credit card numbers
- Clear privacy recommendations

### Reporting
- Detailed assessment results
- Visual representations of findings
- Actionable recommendations
- Downloadable reports

## Dependencies

- Python 3.8+
- Streamlit
- Pandas & NumPy
- Transformers (HuggingFace)
- PyTorch (CPU version)
- Plotly
- SciPy
- Scikit-learn

## Development

To contribute to EthicGuard:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and feature requests, please use the GitHub issue tracker.