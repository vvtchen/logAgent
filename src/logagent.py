"""
LogAgent - Main application for code analysis and error log feedback.
"""

from typing import Optional
from pathlib import Path
import os
from .code_splitter import ASTCodeSplitter
from .embedder import E5Embedder
from .vector_db import QdrantVectorDB
from .indexer import CodeIndexer
from .query_interface import ErrorLogAnalyzer, AnalysisResult


class LogAgent:
    """Main LogAgent application."""

    def __init__(
        self,
        qdrant_host: str = "localhost",
        qdrant_port: int = 6333,
        collection_name: str = "code_chunks",
        use_memory_db: bool = False,
        embedding_model: str = "intfloat/e5-base-v2",
        use_llm: bool = True,
        anthropic_api_key: Optional[str] = None,
        claude_model: str = "claude-sonnet-4-20250514",
        verbose: bool = False,
        save_prompts: bool = False,
        prompts_dir: str = "./prompts"
    ):
        """
        Initialize LogAgent.

        Args:
            qdrant_host: Qdrant server host
            qdrant_port: Qdrant server port
            collection_name: Name of the vector collection
            use_memory_db: Use in-memory database (for testing)
            embedding_model: Name of the embedding model to use
            use_llm: Whether to use Claude for intelligent analysis (default: True)
            anthropic_api_key: Anthropic API key (or set ANTHROPIC_API_KEY env var)
            claude_model: Claude model to use
            verbose: If True, print prompts sent to Claude and responses
            save_prompts: If True, save prompts and responses to files
            prompts_dir: Directory to save prompts (default: ./prompts)
        """
        print("Initializing LogAgent...")

        # Initialize components
        self.embedder = E5Embedder(model_name=embedding_model)
        self.vector_db = QdrantVectorDB(
            host=qdrant_host,
            port=qdrant_port,
            collection_name=collection_name,
            use_memory=use_memory_db
        )
        self.splitter = ASTCodeSplitter()
        self.indexer = CodeIndexer(
            embedder=self.embedder,
            vector_db=self.vector_db,
            splitter=self.splitter
        )

        # Initialize LLM analyzer if requested
        self.llm_analyzer = None
        self.use_llm = use_llm

        if use_llm:
            try:
                from .llm_analyzer import ClaudeAnalyzer

                api_key = anthropic_api_key or os.environ.get("ANTHROPIC_API_KEY")
                if api_key:
                    self.llm_analyzer = ClaudeAnalyzer(
                        api_key=api_key,
                        model=claude_model,
                        verbose=verbose,
                        save_prompts=save_prompts,
                        prompts_dir=prompts_dir
                    )
                    print("✓ Claude AI enabled for intelligent analysis")
                    if verbose:
                        print("  🔍 Verbose mode: Will show prompts and responses")
                    if save_prompts:
                        print(f"  💾 Saving prompts to: {prompts_dir}/")
                else:
                    print("⚠ ANTHROPIC_API_KEY not found. Falling back to rule-based analysis.")
                    print("  Set ANTHROPIC_API_KEY environment variable to enable Claude AI.")
            except Exception as e:
                print(f"⚠ Could not initialize Claude: {e}")
                print("  Falling back to rule-based analysis.")

        # Initialize analyzer with optional LLM
        self.analyzer = ErrorLogAnalyzer(
            indexer=self.indexer,
            llm_analyzer=self.llm_analyzer
        )

        print("LogAgent initialized successfully!")

    def setup(self):
        """Set up the vector database collection."""
        print("Setting up vector database collection...")
        self.indexer.initialize_collection()
        print("Setup complete!")

    def index_codebase(self, codebase_path: str, pattern: str = "**/*.py") -> int:
        """
        Index a codebase for analysis.

        Args:
            codebase_path: Path to the codebase directory
            pattern: Glob pattern for files to index

        Returns:
            Number of code chunks indexed
        """
        path = Path(codebase_path)
        if not path.exists():
            raise FileNotFoundError(f"Codebase path not found: {codebase_path}")

        if path.is_file():
            return self.indexer.index_file(str(path))
        else:
            return self.indexer.index_directory(str(path), pattern=pattern)

    def analyze_error_log(
        self,
        error_log: str,
        num_results: int = 5,
        min_score: float = 0.3,
        show_report: bool = True
    ) -> AnalysisResult:
        """
        Analyze an error log and get advice.

        Args:
            error_log: The error log text
            num_results: Number of relevant code chunks to retrieve
            min_score: Minimum similarity score for relevance
            show_report: Whether to print the formatted report

        Returns:
            AnalysisResult object
        """
        result = self.analyzer.analyze_error(
            error_log=error_log,
            num_results=num_results,
            min_score=min_score
        )

        if show_report:
            print(self.analyzer.format_result(result))

        return result

    def analyze_error_log_file(
        self,
        log_file_path: str,
        num_results: int = 5,
        min_score: float = 0.3,
        show_report: bool = True
    ) -> AnalysisResult:
        """
        Analyze an error log from a file.

        Args:
            log_file_path: Path to the log file
            num_results: Number of relevant code chunks to retrieve
            min_score: Minimum similarity score for relevance
            show_report: Whether to print the formatted report

        Returns:
            AnalysisResult object
        """
        log_path = Path(log_file_path)
        if not log_path.exists():
            raise FileNotFoundError(f"Log file not found: {log_file_path}")

        with open(log_file_path, 'r', encoding='utf-8') as f:
            error_log = f.read()

        return self.analyze_error_log(
            error_log=error_log,
            num_results=num_results,
            min_score=min_score,
            show_report=show_report
        )

    def search_code(self, query: str, limit: int = 5, min_score: float = 0.5):
        """
        Search for code relevant to a query.

        Args:
            query: Search query
            limit: Maximum number of results
            min_score: Minimum similarity score

        Returns:
            List of relevant code chunks
        """
        results = self.indexer.search_similar_code(
            query=query,
            limit=limit,
            score_threshold=min_score
        )

        print(f"\nFound {len(results)} relevant code chunks:\n")
        for i, result in enumerate(results, 1):
            metadata = result['metadata']
            print(f"{i}. {metadata.get('name', 'unknown')} ({result['score']:.2%} match)")
            print(f"   File: {metadata.get('file_path', 'unknown')}")
            print(f"   Type: {metadata.get('chunk_type', 'unknown')}")
            print(f"   Lines: {metadata.get('start_line', '?')}-{metadata.get('end_line', '?')}\n")

        return results

    def get_stats(self):
        """Get statistics about the indexed codebase."""
        info = self.vector_db.get_collection_info()
        print("\nCodebase Statistics:")
        print("-" * 40)
        print(f"Collection: {info.get('name', 'unknown')}")
        print(f"Total chunks: {info.get('points_count', 0)}")
        print(f"Status: {info.get('status', 'unknown')}")
        print("-" * 40)
        return info
