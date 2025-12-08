
#!/usr/bin/env python
"""
Analyze error logs from your project with Claude AI.
Configured for: /home/jayden/aoi
"""

import sys
import os
from dotenv import load_dotenv
from src.logagent import LogAgent

def main():
    # Load environment variables
    load_dotenv()

    print("=" * 80)
    print("LogAgent - AI Error Analysis for /home/jayden/aoi")
    print("=" * 80)
    print()

    # Check for log file argument
    if len(sys.argv) < 2:
        print("Usage: ./run.sh analyze_my_project.py <log_file>")
        print()
        print("Examples:")
        print("  ./run.sh analyze_my_project.py error.log")
        print("  ./run.sh analyze_my_project.py logs-from-cambrian-consumer-image-in-cambrian-inference-list-6f5bddc5c4-mrv8m.log")
        print()
        sys.exit(1)

    log_file = sys.argv[1]

    # Check if log file exists
    if not os.path.exists(log_file):
        print(f"✗ Error: Log file not found: {log_file}")
        print()
        sys.exit(1)

    print(f"📄 Log file: {log_file}")
    print()

    # Initialize LogAgent with Claude AI
    print("Initializing LogAgent with Claude AI...")
    agent = LogAgent(
        use_memory_db=True,      # Fast in-memory database
        use_llm=True,            # Enable Claude AI
        claude_model="claude-sonnet-4-20250514"
    )

    # Setup
    agent.setup()
    print()

    # Index your codebase
    print("=" * 80)
    print("Step 1: Indexing codebase at /home/jayden/aoi")
    print("=" * 80)

    codebase_path = "/home/jayden/aoi"

    if not os.path.exists(codebase_path):
        print(f"⚠ Warning: Codebase path not found: {codebase_path}")
        print("Please update the path in this script or config.py")
        print()
        sys.exit(1)

    num_chunks = agent.index_codebase(codebase_path)
    print(f"\n✓ Indexed {num_chunks} code chunks from {codebase_path}")
    print()

    # Show stats
    agent.get_stats()
    print()

    # Analyze the error log with Claude AI
    print("=" * 80)
    print("Step 2: Analyzing error log with Claude AI")
    print("=" * 80)
    print()

    result = agent.analyze_error_log_file(
        log_file,
        num_results=5,      # Get top 5 relevant code chunks
        min_score=0.3,      # Minimum similarity threshold
        show_report=True    # Print the full report
    )

    print()
    print("=" * 80)
    print("Analysis Complete!")
    print("=" * 80)
    print()

    if result.used_llm:
        print("✓ Claude AI provided intelligent analysis above")
        print(f"✓ Confidence: {result.confidence:.1%}")
        print(f"✓ Model: claude-sonnet-4-20250514")
    else:
        print("⚠ Fell back to rule-based analysis")
        print("  Check your ANTHROPIC_API_KEY in .env file")

    print()


if __name__ == "__main__":
    main()
