#!/bin/bash
# Quick wrapper to analyze error logs with custom codebase

# Usage examples:
#   ./analyze.sh error.log /path/to/code
#   ./analyze.sh error.log ~/myproject/src
#   ./analyze.sh error.log .

# Activate venv
source venv/bin/activate

# Check arguments
if [ $# -lt 2 ]; then
    echo "Usage: $0 <log_file> <codebase_path> [options]"
    echo ""
    echo "Examples:"
    echo "  $0 error.log /home/jayden/myproject/src"
    echo "  $0 error.log ~/myproject/src"
    echo "  $0 error.log . --num-results 10"
    echo "  $0 error.log ../backend/src --min-score 0.2"
    echo ""
    exit 1
fi

LOG_FILE=$1
CODEBASE=$2
shift 2  # Remove first two arguments

# Run with all remaining arguments passed through
python analyze_log.py "$LOG_FILE" --codebase "$CODEBASE" --use-memory "$@"
