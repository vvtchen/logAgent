"""
Query interface for error log analysis and code advice.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from .indexer import CodeIndexer


@dataclass
class AnalysisResult:
    """Result of error log analysis."""
    error_summary: str
    relevant_code: List[Dict[str, Any]]
    advice: str
    confidence: float
    used_llm: bool = False


class ErrorLogAnalyzer:
    """Analyzes error logs and provides code-based advice."""

    def __init__(self, indexer: CodeIndexer, llm_analyzer=None):
        """
        Initialize the error log analyzer.

        Args:
            indexer: Code indexer with access to the codebase
            llm_analyzer: Optional LLM analyzer (e.g., ClaudeAnalyzer) for intelligent advice
        """
        self.indexer = indexer
        self.llm_analyzer = llm_analyzer
        self.use_llm = llm_analyzer is not None

    def analyze_error(
        self,
        error_log: str,
        num_results: int = 5,
        min_score: float = 0.3
    ) -> AnalysisResult:
        """
        Analyze an error log and provide advice.

        Args:
            error_log: The error log text
            num_results: Number of relevant code chunks to retrieve
            min_score: Minimum similarity score for relevance

        Returns:
            AnalysisResult with analysis and advice
        """
        # Extract key information from error log
        error_summary = self._extract_error_summary(error_log)

        # Search for relevant code
        relevant_code = self.indexer.search_similar_code(
            query=error_log,
            limit=num_results,
            score_threshold=min_score
        )

        # Generate advice based on relevant code
        if self.use_llm and self.llm_analyzer:
            # Use LLM for intelligent analysis
            advice = self._generate_llm_advice(error_log, relevant_code)
            used_llm = True
        else:
            # Fall back to rule-based advice
            advice = self._generate_advice(error_log, relevant_code)
            used_llm = False

        # Calculate confidence
        confidence = self._calculate_confidence(relevant_code)

        return AnalysisResult(
            error_summary=error_summary,
            relevant_code=relevant_code,
            advice=advice,
            confidence=confidence,
            used_llm=used_llm
        )

    def _extract_error_summary(self, error_log: str) -> str:
        """
        Extract a summary of the error from the log.

        Args:
            error_log: Full error log text

        Returns:
            Error summary
        """
        lines = error_log.strip().split('\n')

        # Look for common error patterns
        error_indicators = ['Error:', 'Exception:', 'Traceback', 'ERROR', 'FATAL']

        summary_lines = []
        for line in lines:
            for indicator in error_indicators:
                if indicator in line:
                    summary_lines.append(line.strip())
                    break

        if summary_lines:
            return '\n'.join(summary_lines[:5])  # First 5 error lines

        # If no specific error found, return first few lines
        return '\n'.join(lines[:3])

    def _generate_llm_advice(
        self,
        error_log: str,
        relevant_code: List[Dict[str, Any]]
    ) -> str:
        """
        Generate advice using LLM (Claude).

        Args:
            error_log: The error log
            relevant_code: List of relevant code chunks

        Returns:
            AI-generated advice string
        """
        if not relevant_code:
            return (
                "No relevant code found in the indexed codebase. "
                "Please ensure:\n"
                "1. The codebase has been properly indexed\n"
                "2. The error is related to the indexed code\n"
                "3. Try lowering the similarity threshold"
            )

        try:
            # Use LLM to analyze error with context
            analysis = self.llm_analyzer.analyze_error_with_context(
                error_log=error_log,
                relevant_code=relevant_code,
                num_context_chunks=3
            )

            # Add relevant code locations for reference
            advice_parts = [analysis]
            advice_parts.append("\n" + "=" * 80)
            advice_parts.append("RELEVANT CODE LOCATIONS")
            advice_parts.append("=" * 80)

            for i, result in enumerate(relevant_code[:5], 1):
                m = result['metadata']
                advice_parts.append(
                    f"\n{i}. {m.get('file_path', 'unknown')}:{m.get('start_line', '?')}"
                )
                advice_parts.append(f"   Type: {m.get('chunk_type', 'unknown')}")
                advice_parts.append(f"   Name: {m.get('name', 'unknown')}")
                advice_parts.append(f"   Similarity: {result['score']:.2%}")

            return '\n'.join(advice_parts)

        except Exception as e:
            # Fall back to rule-based advice if LLM fails
            print(f"LLM analysis failed: {e}")
            print("Falling back to rule-based advice...")
            return self._generate_advice(error_log, relevant_code)

    def _generate_advice(
        self,
        error_log: str,
        relevant_code: List[Dict[str, Any]]
    ) -> str:
        """
        Generate advice based on error log and relevant code.

        Args:
            error_log: The error log
            relevant_code: List of relevant code chunks

        Returns:
            Advice string
        """
        if not relevant_code:
            return (
                "No relevant code found in the indexed codebase. "
                "Suggestions:\n"
                "1. Ensure the codebase has been properly indexed\n"
                "2. Check if the error is related to external dependencies\n"
                "3. Review the error log for stack traces and line numbers"
            )

        advice_parts = ["Based on the error log and relevant code analysis:\n"]

        # Analyze the top results
        top_result = relevant_code[0]
        metadata = top_result['metadata']

        advice_parts.append(f"\n1. Most relevant code location:")
        advice_parts.append(f"   File: {metadata.get('file_path', 'unknown')}")
        advice_parts.append(f"   Type: {metadata.get('chunk_type', 'unknown')}")
        advice_parts.append(f"   Name: {metadata.get('name', 'unknown')}")
        advice_parts.append(f"   Lines: {metadata.get('start_line', '?')}-{metadata.get('end_line', '?')}")
        advice_parts.append(f"   Relevance: {top_result['score']:.2%}")

        # Provide general recommendations
        advice_parts.append("\n2. Recommended actions:")

        # Analyze error type
        if 'AttributeError' in error_log:
            advice_parts.append("   - Check for None values or missing attributes")
            advice_parts.append("   - Verify object initialization")
        elif 'KeyError' in error_log:
            advice_parts.append("   - Validate dictionary keys before access")
            advice_parts.append("   - Use .get() method with defaults")
        elif 'TypeError' in error_log:
            advice_parts.append("   - Check function argument types")
            advice_parts.append("   - Verify data type conversions")
        elif 'ImportError' in error_log or 'ModuleNotFoundError' in error_log:
            advice_parts.append("   - Verify package installation")
            advice_parts.append("   - Check import paths")
        else:
            advice_parts.append("   - Review the relevant code sections")
            advice_parts.append("   - Check for edge cases and error handling")

        # List other relevant locations
        if len(relevant_code) > 1:
            advice_parts.append("\n3. Other potentially relevant code:")
            for i, result in enumerate(relevant_code[1:4], 1):
                m = result['metadata']
                advice_parts.append(
                    f"   {i}. {m.get('file_path', 'unknown')}:"
                    f"{m.get('start_line', '?')} ({result['score']:.2%} match)"
                )

        return '\n'.join(advice_parts)

    def _calculate_confidence(self, relevant_code: List[Dict[str, Any]]) -> float:
        """
        Calculate confidence score for the analysis.

        Args:
            relevant_code: List of relevant code chunks

        Returns:
            Confidence score between 0 and 1
        """
        if not relevant_code:
            return 0.0

        # Use the top result's score as primary indicator
        top_score = relevant_code[0]['score']

        # Boost confidence if we have multiple relevant results
        num_results = len([r for r in relevant_code if r['score'] > 0.5])
        result_boost = min(num_results * 0.1, 0.3)

        confidence = min(top_score + result_boost, 1.0)
        return confidence

    def analyze_multiple_errors(
        self,
        error_logs: List[str],
        num_results: int = 3
    ) -> List[AnalysisResult]:
        """
        Analyze multiple error logs.

        Args:
            error_logs: List of error log texts
            num_results: Number of results per error

        Returns:
            List of analysis results
        """
        results = []
        for error_log in error_logs:
            result = self.analyze_error(error_log, num_results=num_results)
            results.append(result)

        return results

    def format_result(self, result: AnalysisResult) -> str:
        """
        Format an analysis result for display.

        Args:
            result: AnalysisResult to format

        Returns:
            Formatted string
        """
        output = []
        output.append("=" * 80)
        analysis_type = "AI-POWERED" if result.used_llm else "RULE-BASED"
        output.append(f"ERROR ANALYSIS REPORT ({analysis_type})")
        output.append("=" * 80)

        output.append("\nERROR SUMMARY:")
        output.append("-" * 80)
        output.append(result.error_summary)

        output.append("\n\nANALYSIS CONFIDENCE: {:.1%}".format(result.confidence))
        if result.used_llm:
            output.append("Analysis Method: Claude AI")

        output.append("\n\nRECOMMENDATIONS:")
        output.append("-" * 80)
        output.append(result.advice)

        if result.relevant_code:
            output.append("\n\nRELEVANT CODE DETAILS:")
            output.append("-" * 80)
            for i, code_info in enumerate(result.relevant_code[:3], 1):
                metadata = code_info['metadata']
                output.append(f"\n[{i}] {metadata.get('name', 'unknown')}")
                output.append(f"    File: {metadata.get('file_path', 'unknown')}")
                output.append(f"    Type: {metadata.get('chunk_type', 'unknown')}")
                output.append(f"    Lines: {metadata.get('start_line', '?')}-{metadata.get('end_line', '?')}")
                output.append(f"    Match: {code_info['score']:.2%}")

        output.append("\n" + "=" * 80)

        return '\n'.join(output)
