#!/bin/bash

# Activate virtual environment (if applicable)
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Install required dependencies
pip install -r requirements.txt

# Start the Streamlit application
streamlit run app.py
