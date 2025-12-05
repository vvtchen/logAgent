"""
Example usage of LogAgent with Claude AI integration.

Before running:
1. Install dependencies: pip install -r requirements.txt
2. Set your API key: export ANTHROPIC_API_KEY=your_key_here
3. Or create .env file with: ANTHROPIC_API_KEY=your_key_here
"""

import os
from dotenv import load_dotenv
from src.logagent import LogAgent


def main():
    """Example demonstrating Claude AI-powered error analysis."""

    # Load environment variables from .env file if it exists
    load_dotenv()

    # Check if API key is set
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("=" * 80)
        print("WARNING: ANTHROPIC_API_KEY not found!")
        print("=" * 80)
        print("\nTo enable Claude AI analysis:")
        print("1. Get your API key from: https://console.anthropic.com/")
        print("2. Set it as an environment variable:")
        print("   export ANTHROPIC_API_KEY=your_key_here")
        print("\nOr create a .env file with:")
        print("   ANTHROPIC_API_KEY=your_key_here")
        print("\nContinuing with rule-based analysis...\n")

    print("=" * 80)
    print("LogAgent - AI-Powered Error Analysis with Claude")
    print("=" * 80)

    # Initialize LogAgent with Claude enabled
    agent = LogAgent(
        use_memory_db=True,  # Use in-memory DB for demo
        use_llm=True,        # Enable Claude AI
        embedding_model="intfloat/e5-base-v2"
    )

    # Setup
    agent.setup()

    # Index the codebase
    print("\n" + "=" * 80)
    print("Step 1: Indexing codebase")
    print("=" * 80)

    codebase_path = "./src"
    num_chunks = agent.index_codebase(codebase_path)
    print(f"\nIndexed {num_chunks} code chunks from {codebase_path}")

    # Show stats
    agent.get_stats()

    # Example 1: Analyze a Python error
    print("\n" + "=" * 80)
    print("Step 2: Analyzing Python error with Claude AI")
    print("=" * 80)

    sample_error = """
Traceback (most recent call last):
  File "/home/user/app/main.py", line 87, in process_request
    result = embedder.embed_code(code_snippet)
  File "/home/user/app/embedder.py", line 45, in embed_code
    embedding = self.model.encode(text, normalize_embeddings=True)
AttributeError: 'NoneType' object has no attribute 'encode'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/user/app/main.py", line 92, in process_request
    logger.error("Embedding failed", error=str(e))
TypeError: error() got an unexpected keyword argument 'error'
"""

    print("\nAnalyzing error log with Claude AI...")
    print("-" * 80)

    result = agent.analyze_error_log(sample_error, num_results=5, show_report=True)

    # Example 2: Check if a log file exists and analyze it
    print("\n" + "=" * 80)
    print("Step 3: Analyzing log file (if available)")
    print("=" * 80)

    import glob
    log_files = glob.glob("*.log")

    if log_files:
        log_file = log_files[0]
        print(f"\nFound log file: {log_file}")
        print("Analyzing with Claude AI...\n")
        agent.analyze_error_log_file(log_file, num_results=5, show_report=True)
    else:
        print("\nNo .log files found in current directory")

    # Show comparison
    print("\n" + "=" * 80)
    print("LLM vs Rule-Based Comparison")
    print("=" * 80)
    print("\nAnalysis method used:", "Claude AI" if result.used_llm else "Rule-based")
    print("Confidence score:", f"{result.confidence:.1%}")

    if result.used_llm:
        print("\n✓ Claude AI provided:")
        print("  - Root cause analysis")
        print("  - Specific code recommendations")
        print("  - Context-aware explanations")
        print("  - Actionable fix suggestions")
    else:
        print("\n⚠ Using rule-based analysis")
        print("  Set ANTHROPIC_API_KEY to enable Claude AI for better results")

    print("\n" + "=" * 80)
    print("Demo completed!")
    print("=" * 80)


if __name__ == "__main__":
    main()
