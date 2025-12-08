#!/bin/bash
# Quick script to analyze error logs with Claude AI
# Analyzes codebase at: /home/jayden/aoi

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     LogAgent - Claude AI Error Analysis                           ║${NC}"
echo -e "${BLUE}║     Codebase: /home/jayden/aoi                                     ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if log file provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <log_file>"
    echo ""
    echo "Examples:"
    echo "  $0 error.log"
    echo "  $0 inspect-flow_1204.log"
    echo ""
    exit 1
fi

LOG_FILE=$1

# Check if log file exists
if [ ! -f "$LOG_FILE" ]; then
    echo "✗ Error: Log file not found: $LOG_FILE"
    echo ""
    exit 1
fi

echo -e "${GREEN}✓${NC} Log file: $LOG_FILE"
echo ""

# Activate venv and run
source venv/bin/activate
python analyze_my_project.py "$LOG_FILE"
