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
        model: str = "claude-sonnet-4-20250514",
        max_tokens: int = 2000,
        verbose: bool = False,
        save_prompts: bool = False,
        prompts_dir: str = "./prompts"
    ):
        """
        Initialize Claude analyzer.

        Args:
            api_key: Anthropic API key (or set ANTHROPIC_API_KEY env var)
            model: Claude model to use
            max_tokens: Maximum tokens for response
            verbose: If True, print prompts being sent to Claude
            save_prompts: If True, save prompts and responses to files
            prompts_dir: Directory to save prompts (default: ./prompts)
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
        self.verbose = verbose
        self.save_prompts = save_prompts
        self.prompts_dir = prompts_dir
        self.prompt_counter = 0

        # Create prompts directory if needed
        if self.save_prompts:
            import os
            os.makedirs(self.prompts_dir, exist_ok=True)

    def analyze_error_with_context(
        self,
        error_summary: str,
        relevant_code: List[Dict[str, Any]],
        num_context_chunks: int = 3
    ) -> str:
        """
        Analyze error summary with code context using Claude.

        Args:
            error_summary: Extracted error summary (key error lines only, NOT full log)
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

            # Get the actual code content from metadata
            code_content = metadata.get('content', '# Code content not available')

            context_parts.append(
                f"\n## Relevant Code Chunk {i} (Similarity: {score:.1%})\n"
                f"**File:** {metadata.get('file_path', 'unknown')}\n"
                f"**Type:** {metadata.get('chunk_type', 'unknown')}\n"
                f"**Name:** {metadata.get('name', 'unknown')}\n"
                f"**Lines:** {metadata.get('start_line', '?')}-{metadata.get('end_line', '?')}\n"
                f"**Parent:** {metadata.get('parent_context', 'N/A')}\n"
                f"\n```python\n"
                f"{code_content}\n"
                f"```\n"
            )

        code_context = "\n".join(context_parts)

        # Build the prompt for Claude
        prompt = f"""You are an expert software engineer analyzing error logs and providing actionable debugging advice.

# Error Summary

The following error summary has been automatically extracted from the log file (showing only the key error lines):

```
{error_summary}
```

**Note**: This is a concise summary of the error, not the complete log file. It contains the most relevant error messages and tracebacks.

# Relevant Code Context

The following code chunks were identified as most relevant to this error using semantic vector search. These are the actual code snippets from the codebase that are most similar to the error:

{code_context}

# Your Task

Analyze this error summary in the context of the actual code shown above and provide:

1. **Root Cause Analysis**: What is causing this error?
2. **Specific Location**: Which file, function, and line numbers are involved?
3. **Explanation**: Why is this happening? What's the underlying issue?
4. **Recommended Fix**: Provide specific, actionable steps to fix the issue
5. **Code Suggestion**: If applicable, suggest actual code changes
6. **Prevention**: How to prevent similar errors in the future

Be specific, practical, and reference the actual file paths and code chunks provided above.
"""

        # Increment counter for this request
        self.prompt_counter += 1
        request_id = self.prompt_counter

        # Print prompt if verbose mode
        if self.verbose:
            print("\n" + "=" * 80)
            print(f"📤 PROMPT SENT TO CLAUDE (Request #{request_id})")
            print("=" * 80)
            print(f"Model: {self.model}")
            print(f"Max tokens: {self.max_tokens}")
            print(f"Prompt length: {len(prompt)} characters")
            print("-" * 80)
            print(prompt)
            print("=" * 80)
            print()

        # Save prompt to file if enabled
        if self.save_prompts:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            prompt_file = f"{self.prompts_dir}/prompt_{timestamp}_{request_id}.txt"

            with open(prompt_file, 'w', encoding='utf-8') as f:
                f.write(f"REQUEST #{request_id}\n")
                f.write(f"Timestamp: {timestamp}\n")
                f.write(f"Model: {self.model}\n")
                f.write(f"Max tokens: {self.max_tokens}\n")
                f.write("=" * 80 + "\n")
                f.write("PROMPT:\n")
                f.write("=" * 80 + "\n")
                f.write(prompt)
                f.write("\n\n")

        try:
            # Call Claude API
            if self.verbose:
                print(f"⏳ Sending request to Claude API...")
                print()

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

            # Print response if verbose mode
            if self.verbose:
                print("\n" + "=" * 80)
                print(f"📥 RESPONSE FROM CLAUDE (Request #{request_id})")
                print("=" * 80)
                print(f"Response length: {len(response_text)} characters")
                print(f"Tokens used: {message.usage.input_tokens} input, {message.usage.output_tokens} output")
                print("-" * 80)
                print(response_text)
                print("=" * 80)
                print()

            # Save response to file if enabled
            if self.save_prompts:
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                response_file = f"{self.prompts_dir}/response_{timestamp}_{request_id}.txt"

                with open(response_file, 'w', encoding='utf-8') as f:
                    f.write(f"RESPONSE #{request_id}\n")
                    f.write(f"Timestamp: {timestamp}\n")
                    f.write(f"Model: {self.model}\n")
                    f.write(f"Tokens: {message.usage.input_tokens} input, {message.usage.output_tokens} output\n")
                    f.write("=" * 80 + "\n")
                    f.write("RESPONSE:\n")
                    f.write("=" * 80 + "\n")
                    f.write(response_text)
                    f.write("\n")

                # Also save a combined file
                combined_file = f"{self.prompts_dir}/conversation_{timestamp}_{request_id}.txt"
                with open(combined_file, 'w', encoding='utf-8') as f:
                    f.write(f"CLAUDE API CONVERSATION #{request_id}\n")
                    f.write(f"Timestamp: {timestamp}\n")
                    f.write(f"Model: {self.model}\n")
                    f.write("=" * 80 + "\n\n")
                    f.write("PROMPT:\n")
                    f.write("=" * 80 + "\n")
                    f.write(prompt)
                    f.write("\n\n")
                    f.write("=" * 80 + "\n")
                    f.write("RESPONSE:\n")
                    f.write("=" * 80 + "\n")
                    f.write(response_text)
                    f.write("\n\n")
                    f.write("=" * 80 + "\n")
                    f.write(f"TOKENS: {message.usage.input_tokens} input, {message.usage.output_tokens} output\n")

                if self.verbose:
                    print(f"💾 Saved conversation to: {combined_file}")
                    print()

            return response_text

        except Exception as e:
            error_msg = f"Error calling Claude API: {str(e)}\n\nFalling back to basic analysis..."

            if self.verbose:
                print("\n" + "=" * 80)
                print(f"❌ ERROR (Request #{request_id})")
                print("=" * 80)
                print(error_msg)
                print("=" * 80)
                print()

            if self.save_prompts:
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                error_file = f"{self.prompts_dir}/error_{timestamp}_{request_id}.txt"
                with open(error_file, 'w', encoding='utf-8') as f:
                    f.write(f"ERROR #{request_id}\n")
                    f.write(f"Timestamp: {timestamp}\n")
                    f.write("=" * 80 + "\n")
                    f.write(error_msg)

            return error_msg

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
