"""
Standalone script to analyze a specific error log file.
"""

import sys
import argparse
from pathlib import Path
from src.logagent import LogAgent


def main():
    """Analyze an error log file."""
    parser = argparse.ArgumentParser(
        description="Analyze error logs using LogAgent"
    )
    parser.add_argument(
        "log_file",
        help="Path to the error log file"
    )
    parser.add_argument(
        "--codebase",
        default="./src",
        help="Path to codebase to index (default: ./src)"
    )
    parser.add_argument(
        "--num-results",
        type=int,
        default=5,
        help="Number of relevant code chunks to retrieve (default: 5)"
    )
    parser.add_argument(
        "--min-score",
        type=float,
        default=0.2,
        help="Minimum similarity score (default: 0.2)"
    )
    parser.add_argument(
        "--use-memory",
        action="store_true",
        help="Use in-memory database instead of Qdrant server"
    )
    parser.add_argument(
        "--model",
        default="intfloat/e5-base-v2",
        help="Embedding model to use (default: intfloat/e5-base-v2)"
    )

    args = parser.parse_args()

    # Check if log file exists
    log_path = Path(args.log_file)
    if not log_path.exists():
        print(f"Error: Log file not found: {args.log_file}")
        sys.exit(1)

    # Initialize LogAgent
    print("Initializing LogAgent...")
    agent = LogAgent(
        use_memory_db=args.use_memory,
        embedding_model=args.model
    )

    # Setup
    agent.setup()

    # Index codebase
    print(f"\nIndexing codebase: {args.codebase}")
    codebase_path = Path(args.codebase)
    if codebase_path.exists():
        num_chunks = agent.index_codebase(str(codebase_path))
        print(f"Indexed {num_chunks} code chunks")
    else:
        print(f"Warning: Codebase path not found: {args.codebase}")
        print("Proceeding without indexing...")

    # Show stats
    agent.get_stats()

    # Analyze the log file
    print(f"\nAnalyzing error log: {args.log_file}")
    print("=" * 80)

    result = agent.analyze_error_log_file(
        args.log_file,
        num_results=args.num_results,
        min_score=args.min_score,
        show_report=True
    )

    # Additional recommendations
    print("\n" + "=" * 80)
    print("NEXT STEPS:")
    print("=" * 80)
    print("1. Review the relevant code sections identified above")
    print("2. Check the specific line numbers mentioned in the error")
    print("3. Consider adding error handling for edge cases")
    print("4. Run tests after making changes")
    print("=" * 80)


if __name__ == "__main__":
    main()
