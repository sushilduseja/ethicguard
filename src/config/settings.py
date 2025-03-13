import os

# Example: Set your API key for any external services (if using OpenAI, etc.)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your_default_api_key")

# Configure log level (can be customized via environment variable)
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Application settings
APP_NAME = "EthicGuard"
DEBUG = True

# Logging configuration
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_FILENAME = 'ethicguard_{date}.log'

# Metric thresholds
THRESHOLDS = {
    'bias': {
        'high': 0.8,  # Above this is good (low bias)
        'moderate': 0.6  # Below this is bad (high bias)
    },
    'fairness': {
        'high': 0.8,  # Above this is fair
        'moderate': 0.6  # Below this is unfair
    },
    'documentation': {
        'complete': 0.8,
        'partial': 0.5
    }
}

# Documentation requirements
REQUIRED_SECTIONS = {
    'purpose': ['purpose', 'objective', 'goal'],
    'data': ['data', 'dataset', 'collection'],
    'limitations': ['limitation', 'constraint', 'bias', 'issue']
}

# UI Elements
UI_ELEMENTS = {
    'ratings': {
        'good': '✅',
        'warning': '⚠️',
        'error': '❌'
    },
    'messages': {
        'no_data': "Please provide at least 2 data points",
        'missing_group': "Missing data for one or more groups",
        'success': "✅ Assessment Complete!"
    }
}
