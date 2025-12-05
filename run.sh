#!/bin/bash
# Helper script to run LogAgent with correct environment

# Activate virtual environment
source venv/bin/activate

# Run the command passed as argument, or main.py by default
if [ $# -eq 0 ]; then
    python main.py
else
    python "$@"
fi
