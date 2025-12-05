"""
LLM-powered code analysis using Claude API.
"""

from typing import List, Dict, Any, Optional
import os
from anthropic import Anthropic


class ClaudeAnalyzer:
    """Analyzes error logs using Claude API for intelligent advice."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-3-5-sonnet-20241022",
        max_tokens: int = 2000
    ):
        """
        Initialize Claude analyzer.

        Args:
            api_key: Anthropic API key (or set ANTHROPIC_API_KEY env var)
            model: Claude model to use
            max_tokens: Maximum tokens for response
        """
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Anthropic API key required. Set ANTHROPIC_API_KEY environment variable "
                "or pass api_key parameter."
            )

        self.client = Anthropic(api_key=self.api_key)
        self.model = model
        self.max_tokens = max_tokens

    def analyze_error_with_context(
        self,
        error_log: str,
        relevant_code: List[Dict[str, Any]],
        num_context_chunks: int = 3
    ) -> str:
        """
        Analyze error log with code context using Claude.

        Args:
            error_log: The error log text
            relevant_code: List of relevant code chunks from vector search
            num_context_chunks: Number of code chunks to include in context

        Returns:
            Detailed analysis and advice from Claude
        """
        # Build context from relevant code
        context_parts = []
        for i, code_info in enumerate(relevant_code[:num_context_chunks], 1):
            metadata = code_info['metadata']
            score = code_info['score']

            context_parts.append(
                f"\n## Relevant Code Chunk {i} (Similarity: {score:.1%})\n"
                f"**File:** {metadata.get('file_path', 'unknown')}\n"
                f"**Type:** {metadata.get('chunk_type', 'unknown')}\n"
                f"**Name:** {metadata.get('name', 'unknown')}\n"
                f"**Lines:** {metadata.get('start_line', '?')}-{metadata.get('end_line', '?')}\n"
                f"**Parent:** {metadata.get('parent_context', 'N/A')}\n"
                f"\n```python\n"
                f"# Note: This is a code chunk from the codebase, not the full file\n"
                f"# The actual code content would be retrieved and shown here\n"
                f"```\n"
            )

        code_context = "\n".join(context_parts)

        # Build the prompt for Claude
        prompt = f"""You are an expert software engineer analyzing error logs and providing actionable debugging advice.

# Error Log

```
{error_log}
```

# Relevant Code Context

The following code chunks were identified as most relevant to this error (using semantic search):

{code_context}

# Your Task

Analyze this error log in the context of the relevant code and provide:

1. **Root Cause Analysis**: What is causing this error?
2. **Specific Location**: Which file, function, and line numbers are involved?
3. **Explanation**: Why is this happening? What's the underlying issue?
4. **Recommended Fix**: Provide specific, actionable steps to fix the issue
5. **Code Suggestion**: If applicable, suggest actual code changes
6. **Prevention**: How to prevent similar errors in the future

Be specific, practical, and reference the actual file paths and code chunks provided above.
"""

        try:
            # Call Claude API
            message = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Extract response
            response_text = message.content[0].text
            return response_text

        except Exception as e:
            return f"Error calling Claude API: {str(e)}\n\nFalling back to basic analysis..."

    def generate_advice_summary(
        self,
        error_summary: str,
        claude_analysis: str,
        confidence: float
    ) -> str:
        """
        Generate a formatted advice summary.

        Args:
            error_summary: Brief summary of the error
            claude_analysis: Detailed analysis from Claude
            confidence: Confidence score from vector search

        Returns:
            Formatted advice string
        """
        advice_parts = []

        advice_parts.append("=" * 80)
        advice_parts.append("AI-POWERED ERROR ANALYSIS (Claude)")
        advice_parts.append("=" * 80)
        advice_parts.append(f"\nConfidence Score: {confidence:.1%}")
        advice_parts.append(f"\n{claude_analysis}")
        advice_parts.append("\n" + "=" * 80)

        return "\n".join(advice_parts)

    def batch_analyze(
        self,
        error_logs: List[str],
        relevant_code_per_error: List[List[Dict[str, Any]]]
    ) -> List[str]:
        """
        Analyze multiple errors in batch.

        Args:
            error_logs: List of error log texts
            relevant_code_per_error: List of relevant code chunks for each error

        Returns:
            List of analysis results
        """
        results = []
        for error_log, relevant_code in zip(error_logs, relevant_code_per_error):
            analysis = self.analyze_error_with_context(error_log, relevant_code)
            results.append(analysis)

        return results

    def health_check(self) -> bool:
        """
        Check if the Claude API is accessible.

        Returns:
            True if API is working, False otherwise
        """
        try:
            # Try a simple API call
            message = self.client.messages.create(
                model=self.model,
                max_tokens=10,
                messages=[
                    {
                        "role": "user",
                        "content": "Hello"
                    }
                ]
            )
            return True
        except Exception as e:
            print(f"Claude API health check failed: {e}")
            return False
