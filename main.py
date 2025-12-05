"""
LogAgent - AI-powered code analysis and error log feedback system.

Example usage demonstrating the main features:
1. Index a codebase
2. Analyze error logs
3. Search for relevant code
"""

from src.logagent import LogAgent


def main():
    """Main entry point for LogAgent."""

    # Initialize LogAgent with in-memory database for demo
    print("=" * 80)
    print("LogAgent - AI Code Analysis & Error Log Feedback System")
    print("=" * 80)

    agent = LogAgent(
        use_memory_db=True,  # Use in-memory DB for demo (set to False for production)
        embedding_model="intfloat/e5-base-v2"
    )

    # Setup the vector database
    agent.setup()

    # Example 1: Index the current codebase
    print("\n" + "=" * 80)
    print("STEP 1: Indexing codebase")
    print("=" * 80)

    codebase_path = "./src"  # Index our own source code
    num_chunks = agent.index_codebase(codebase_path)
    print(f"\nIndexed {num_chunks} code chunks from {codebase_path}")

    # Show stats
    agent.get_stats()

    # Example 2: Analyze an error log file
    print("\n" + "=" * 80)
    print("STEP 2: Analyzing error log")
    print("=" * 80)

    # Check if there's a log file to analyze
    import os
    log_files = [f for f in os.listdir('.') if f.endswith('.log')]

    if log_files:
        log_file = log_files[0]
        print(f"\nAnalyzing log file: {log_file}\n")
        result = agent.analyze_error_log_file(log_file, num_results=5)
    else:
        # Use a sample error log
        sample_error = """
        Traceback (most recent call last):
          File "main.py", line 42, in process_data
            result = data['key'].process()
        AttributeError: 'NoneType' object has no attribute 'process'
        """
        print("\nAnalyzing sample error log:\n")
        result = agent.analyze_error_log(sample_error, num_results=5)

    # Example 3: Search for specific code
    print("\n" + "=" * 80)
    print("STEP 3: Searching for relevant code")
    print("=" * 80)

    query = "embedding generation"
    print(f"\nSearching for: '{query}'\n")
    agent.search_code(query, limit=3)

    print("\n" + "=" * 80)
    print("Demo completed!")
    print("=" * 80)


if __name__ == '__main__':
    main()
